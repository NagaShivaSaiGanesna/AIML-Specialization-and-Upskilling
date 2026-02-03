"""
Document Q&A System - Production Quality
No embeddings required - uses context injection with smart chunking

Author: AI Assistant
Date: 2024
"""

import os
import sys
from typing import List, Dict, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Document processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

# LLM and chains
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Utilities
import re
from collections import Counter
from datetime import datetime


class DocumentQASystem:
    """
    Main class for document Q&A without embeddings.
    Uses smart chunking and context injection.
    """
    
    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the Q&A system.
        
        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env variable)
            model: Claude model to use
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required! Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter"
            )
        
        self.model = model
        self.llm = ChatAnthropic(
            model=self.model,
            anthropic_api_key=self.api_key,
            temperature=0
        )
        
        # Smart text splitter - recursive with semantic awareness
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,  # Optimal size for context
            chunk_overlap=300,  # Overlap to maintain context
            length_function=len,
            separators=[
                "\n\n",  # Paragraphs first
                "\n",    # Then lines
                ". ",    # Then sentences
                ", ",    # Then clauses
                " ",     # Then words
                ""       # Finally characters
            ],
            is_separator_regex=False
        )
        
        # Store loaded documents
        self.documents: List[Dict] = []
        self.all_chunks: List[Dict] = []
        
        print(f"✅ DocumentQA System initialized with model: {self.model}")
    
    
    def load_document(self, file_path: str) -> Dict:
        """
        Load a document from file path.
        Supports: PDF, DOCX, TXT
        
        Args:
            file_path: Path to the document
            
        Returns:
            Dictionary with document info
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"\n📄 Loading: {file_path.name}")
        
        try:
            # Choose loader based on file extension
            suffix = file_path.suffix.lower()
            
            if suffix == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif suffix == '.docx':
                loader = Docx2txtLoader(str(file_path))
            elif suffix == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            else:
                raise ValueError(f"Unsupported file type: {suffix}")
            
            # Load document
            raw_docs = loader.load()
            
            # Combine all pages/sections into one text
            full_text = "\n\n".join([doc.page_content for doc in raw_docs])
            
            # Create smart chunks
            chunks = self.text_splitter.create_documents([full_text])
            
            # Add metadata to chunks
            chunk_dicts = []
            for idx, chunk in enumerate(chunks):
                chunk_dict = {
                    'content': chunk.page_content,
                    'chunk_id': idx,
                    'document_name': file_path.name,
                    'char_count': len(chunk.page_content),
                    'word_count': len(chunk.page_content.split())
                }
                chunk_dicts.append(chunk_dict)
                self.all_chunks.append(chunk_dict)
            
            # Store document info
            doc_info = {
                'file_name': file_path.name,
                'file_path': str(file_path),
                'loaded_at': datetime.now().isoformat(),
                'full_text': full_text,
                'chunks': chunk_dicts,
                'total_chunks': len(chunk_dicts),
                'total_chars': len(full_text),
                'total_words': len(full_text.split())
            }
            
            self.documents.append(doc_info)
            
            print(f"✅ Loaded successfully!")
            print(f"   📊 Stats: {len(chunk_dicts)} chunks, "
                  f"{len(full_text.split())} words, "
                  f"{len(full_text):,} characters")
            
            return doc_info
            
        except Exception as e:
            print(f"❌ Error loading {file_path.name}: {str(e)}")
            raise
    
    
    def load_multiple_documents(self, file_paths: List[str]) -> List[Dict]:
        """
        Load multiple documents at once.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of document info dictionaries
        """
        results = []
        for path in file_paths:
            try:
                result = self.load_document(path)
                results.append(result)
            except Exception as e:
                print(f"⚠️  Skipping {path}: {str(e)}")
                continue
        
        return results
    
    
    def _calculate_relevance_score(self, query: str, chunk_text: str) -> float:
        """
        Calculate relevance score using TF-IDF-like approach.
        
        Args:
            query: User's question
            chunk_text: Text chunk to score
            
        Returns:
            Relevance score (0-1)
        """
        # Normalize texts
        query_lower = query.lower()
        chunk_lower = chunk_text.lower()
        
        # Extract query terms (remove common stop words)
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                      'would', 'could', 'should', 'may', 'might', 'must', 'can',
                      'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                      'into', 'through', 'during', 'before', 'after', 'above', 'below',
                      'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under'}
        
        query_terms = [word for word in re.findall(r'\b\w+\b', query_lower) 
                       if word not in stop_words and len(word) > 2]
        
        if not query_terms:
            return 0.0
        
        # Count term frequencies
        chunk_words = re.findall(r'\b\w+\b', chunk_lower)
        chunk_word_freq = Counter(chunk_words)
        
        # Calculate score
        score = 0.0
        for term in query_terms:
            # Exact match
            if term in chunk_lower:
                score += chunk_word_freq[term] * 2.0
            
            # Partial match (for compound words)
            for word in chunk_words:
                if term in word or word in term:
                    score += 0.5
        
        # Normalize by query length and chunk length
        score = score / (len(query_terms) * (len(chunk_words) / 100))
        
        return min(score, 1.0)  # Cap at 1.0
    
    
    def find_relevant_chunks(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Find most relevant chunks for a query using keyword matching.
        
        Args:
            query: User's question
            top_k: Number of top chunks to return
            
        Returns:
            List of relevant chunks with scores
        """
        if not self.all_chunks:
            raise ValueError("No documents loaded! Load documents first.")
        
        # Score all chunks
        scored_chunks = []
        for chunk in self.all_chunks:
            score = self._calculate_relevance_score(query, chunk['content'])
            if score > 0:  # Only include chunks with some relevance
                scored_chunks.append({
                    **chunk,
                    'relevance_score': score
                })
        
        # Sort by score and return top_k
        scored_chunks.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_chunks[:top_k]
    
    
    def ask_question(self, question: str, top_k: int = 5, 
                     show_sources: bool = True) -> Dict:
        """
        Ask a question about the loaded documents.
        
        Args:
            question: The question to ask
            top_k: Number of relevant chunks to use
            show_sources: Whether to return source chunks
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.documents:
            raise ValueError("No documents loaded! Load documents first using load_document()")
        
        print(f"\n🤔 Question: {question}")
        print(f"🔍 Searching through {len(self.all_chunks)} chunks...")
        
        # Find relevant chunks
        relevant_chunks = self.find_relevant_chunks(question, top_k=top_k)
        
        if not relevant_chunks:
            return {
                'answer': "I couldn't find relevant information in the documents to answer this question.",
                'confidence': 'low',
                'sources': [],
                'question': question
            }
        
        print(f"✅ Found {len(relevant_chunks)} relevant chunks")
        
        # Prepare context from chunks
        context_parts = []
        for i, chunk in enumerate(relevant_chunks):
            context_parts.append(
                f"[Document: {chunk['document_name']}, Chunk {chunk['chunk_id']}]\n"
                f"{chunk['content']}\n"
            )
        
        context = "\n---\n".join(context_parts)
        
        # Create prompt using LCEL
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that answers questions based on provided document excerpts.

Instructions:
1. Answer the question using ONLY the information from the provided context
2. If the context doesn't contain enough information, say so clearly
3. Be specific and cite which document/chunk you're referencing when possible
4. If multiple documents have relevant info, synthesize them
5. Keep answers concise but complete"""),
            ("user", """Context from documents:
{context}

Question: {question}

Answer the question based on the context above. Be specific and helpful.""")
        ])
        
        # Create LCEL chain
        chain = (
            {"context": lambda x: x["context"], "question": lambda x: x["question"]}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Get answer
        print("💭 Generating answer...")
        answer = chain.invoke({"context": context, "question": question})
        
        # Prepare response
        response = {
            'answer': answer,
            'question': question,
            'chunks_used': len(relevant_chunks),
            'documents_searched': len(self.documents),
            'confidence': 'high' if relevant_chunks[0]['relevance_score'] > 0.5 else 'medium'
        }
        
        if show_sources:
            response['sources'] = [
                {
                    'document': chunk['document_name'],
                    'chunk_id': chunk['chunk_id'],
                    'relevance_score': round(chunk['relevance_score'], 3),
                    'preview': chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content']
                }
                for chunk in relevant_chunks
            ]
        
        return response
    
    
    def get_document_summary(self) -> str:
        """
        Get a summary of all loaded documents.
        
        Returns:
            Formatted summary string
        """
        if not self.documents:
            return "No documents loaded."
        
        summary = "\n📚 LOADED DOCUMENTS SUMMARY\n" + "="*50 + "\n"
        
        for i, doc in enumerate(self.documents, 1):
            summary += f"\n{i}. {doc['file_name']}\n"
            summary += f"   • Chunks: {doc['total_chunks']}\n"
            summary += f"   • Words: {doc['total_words']:,}\n"
            summary += f"   • Characters: {doc['total_chars']:,}\n"
            summary += f"   • Loaded: {doc['loaded_at']}\n"
        
        summary += f"\n📊 TOTAL: {len(self.documents)} documents, {len(self.all_chunks)} chunks\n"
        
        return summary
    
    
    def clear_documents(self):
        """Clear all loaded documents."""
        self.documents = []
        self.all_chunks = []
        print("🗑️  All documents cleared")


def print_banner():
    """Print welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        📚 DOCUMENT Q&A SYSTEM (No Embeddings)            ║
║                                                           ║
║    Smart chunking + Context injection + Claude AI        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def interactive_mode(qa_system: DocumentQASystem):
    """
    Run interactive Q&A session.
    
    Args:
        qa_system: Initialized DocumentQASystem instance
    """
    print("\n💬 INTERACTIVE MODE")
    print("="*60)
    print("Commands:")
    print("  - Type your question and press Enter")
    print("  - Type 'load <file_path>' to load a new document")
    print("  - Type 'summary' to see loaded documents")
    print("  - Type 'clear' to clear all documents")
    print("  - Type 'quit' or 'exit' to quit")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n❓ You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            elif user_input.lower() == 'summary':
                print(qa_system.get_document_summary())
            
            elif user_input.lower() == 'clear':
                qa_system.clear_documents()
            
            elif user_input.lower().startswith('load '):
                file_path = user_input[5:].strip()
                qa_system.load_document(file_path)
            
            else:
                # Treat as question
                if not qa_system.documents:
                    print("⚠️  No documents loaded! Use 'load <file_path>' first.")
                    continue
                
                result = qa_system.ask_question(user_input)
                
                print(f"\n🤖 Answer ({result['confidence']} confidence):")
                print("-" * 60)
                print(result['answer'])
                print("-" * 60)
                
                if 'sources' in result and result['sources']:
                    print(f"\n📚 Sources ({result['chunks_used']} chunks):")
                    for i, source in enumerate(result['sources'][:3], 1):
                        print(f"\n{i}. {source['document']} (Chunk {source['chunk_id']}) "
                              f"[Score: {source['relevance_score']}]")
                        print(f"   {source['preview']}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def main():
    """Main function - demonstrates usage."""
    print_banner()
    
    # Check for API key
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set!")
        print("\nPlease set it using:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'  # Linux/Mac")
        print("  set ANTHROPIC_API_KEY=your-api-key-here       # Windows CMD")
        print("  $env:ANTHROPIC_API_KEY='your-api-key-here'   # Windows PowerShell")
        sys.exit(1)
    
    try:
        # Initialize system
        qa_system = DocumentQASystem()
        
        # Check for command line arguments
        if len(sys.argv) > 1:
            print("\n📂 Loading documents from command line...")
            files = sys.argv[1:]
            qa_system.load_multiple_documents(files)
        else:
            print("\n💡 TIP: You can pass file paths as arguments:")
            print("   python document_qa.py doc1.pdf doc2.txt doc3.docx")
        
        # Start interactive mode
        interactive_mode(qa_system)
    
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()