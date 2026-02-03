"""
Run this script to create example documents for testing.
Usage: python create_example_docs.py
"""

def create_example_documents():
    """Create sample documents for testing the Q&A system."""
    
    # Example 1: Climate Change Report
    climate_doc = """Climate Change: An Overview

Introduction
Climate change represents one of the most pressing challenges facing humanity in the 21st century. The scientific consensus is clear: global temperatures are rising at an unprecedented rate, primarily due to human activities.

Causes of Climate Change
The primary driver of recent climate change is the emission of greenhouse gases, particularly carbon dioxide (CO2) and methane (CH4). These emissions come from various sources:

1. Fossil Fuel Combustion: The burning of coal, oil, and natural gas for energy and transportation accounts for approximately 75% of global CO2 emissions.

2. Deforestation: The clearing of forests for agriculture and development removes trees that absorb CO2, while also releasing stored carbon.

3. Industrial Processes: Manufacturing, cement production, and chemical processes release significant amounts of greenhouse gases.

4. Agriculture: Livestock farming produces methane, while fertilizer use releases nitrous oxide, both potent greenhouse gases.

Current Impacts
The effects of climate change are already visible worldwide:

Temperature Rise: Global average temperatures have increased by approximately 1.1°C since pre-industrial times.

Extreme Weather: Hurricanes, droughts, floods, and heat waves are becoming more frequent and severe.

Sea Level Rise: Oceans have risen by about 20 cm since 1900, threatening coastal communities.

Ecosystem Disruption: Many species are struggling to adapt, leading to shifts in biodiversity and ecosystem collapse in some regions.

Solutions and Mitigation
Addressing climate change requires coordinated global action:

Renewable Energy: Transitioning to solar, wind, hydroelectric, and other renewable energy sources can dramatically reduce emissions.

Energy Efficiency: Improving efficiency in buildings, transportation, and industry can significantly cut energy demand.

Carbon Capture: Technologies to capture and store carbon dioxide can help reduce atmospheric concentrations.

Reforestation: Planting trees and restoring forests helps absorb CO2 and restore ecosystems.

Sustainable Agriculture: Adopting practices that reduce emissions while maintaining food production is crucial.

International Cooperation
The Paris Agreement, signed in 2015, represents a landmark in international climate action. Countries committed to limiting global temperature rise to well below 2°C above pre-industrial levels, with efforts to limit it to 1.5°C.

Conclusion
Climate change is a complex challenge that requires immediate and sustained action. While the scientific evidence is clear, political will and public engagement remain critical to implementing effective solutions. The decisions we make today will determine the world we leave for future generations."""

    with open("climate_change.txt", "w", encoding="utf-8") as f:
        f.write(climate_doc)
    
    # Example 2: Machine Learning Basics
    ml_doc = """Machine Learning: A Beginner's Guide

What is Machine Learning?
Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. Instead of following rigid instructions, machine learning systems use algorithms to analyze data, identify patterns, and make decisions.

Types of Machine Learning

1. Supervised Learning
In supervised learning, the algorithm learns from labeled training data. The system is provided with input-output pairs and learns to map inputs to correct outputs.

Common Applications:
- Image classification (identifying objects in photos)
- Spam detection (filtering unwanted emails)
- Credit scoring (predicting loan default risk)
- Medical diagnosis (identifying diseases from symptoms)

Popular Algorithms:
- Linear Regression: Predicts continuous values
- Logistic Regression: Classification tasks
- Decision Trees: Rule-based decision making
- Random Forests: Ensemble of decision trees
- Support Vector Machines (SVM): Classification with maximum margin
- Neural Networks: Complex pattern recognition

2. Unsupervised Learning
Unsupervised learning works with unlabeled data, finding hidden patterns or structures without explicit guidance.

Common Applications:
- Customer segmentation (grouping similar customers)
- Anomaly detection (identifying unusual patterns)
- Dimensionality reduction (simplifying complex data)
- Recommendation systems (suggesting products or content)

Popular Algorithms:
- K-Means Clustering: Grouping similar data points
- Hierarchical Clustering: Creating cluster hierarchies
- Principal Component Analysis (PCA): Reducing dimensions
- Association Rules: Finding relationships in data

3. Reinforcement Learning
Reinforcement learning involves training agents to make sequences of decisions by rewarding desired behaviors and punishing undesired ones.

Common Applications:
- Game playing (chess, Go, video games)
- Robotics (autonomous navigation)
- Resource management (optimizing energy usage)
- Trading algorithms (stock market decisions)

Key Concepts

Training Data
The quality and quantity of training data significantly impact model performance. More diverse, representative data generally leads to better results.

Features
Features are the input variables used for prediction. Feature engineering—creating and selecting relevant features—is crucial for model success.

Overfitting and Underfitting
Overfitting occurs when a model learns training data too well, including noise, resulting in poor generalization. Underfitting happens when a model is too simple to capture underlying patterns.

Validation and Testing
Models should be evaluated on separate validation and test sets to ensure they generalize well to new, unseen data.

Popular Machine Learning Frameworks

TensorFlow: Google's open-source framework for deep learning
PyTorch: Facebook's flexible deep learning platform
Scikit-learn: Python library for traditional machine learning
Keras: High-level neural network API

Getting Started

1. Learn Python programming basics
2. Study statistics and linear algebra fundamentals
3. Take online courses (Coursera, edX, fast.ai)
4. Work on practical projects with real datasets
5. Participate in Kaggle competitions
6. Join machine learning communities online

Common Challenges

Data Quality: Ensuring clean, accurate, representative data
Computational Resources: Training complex models requires significant computing power
Model Selection: Choosing appropriate algorithms for specific problems
Interpretability: Understanding why models make certain predictions
Bias and Fairness: Ensuring models don't perpetuate harmful biases

Future Trends

The field continues to evolve rapidly with developments in:
- Transformer models and large language models
- Few-shot and zero-shot learning
- Federated learning for privacy
- AutoML for automated model development
- Edge computing for on-device ML

Conclusion
Machine learning is transforming industries and creating new possibilities. While powerful, it requires careful consideration of ethics, fairness, and societal impact. As the field advances, responsible development and deployment become increasingly important."""

    with open("machine_learning.txt", "w", encoding="utf-8") as f:
        f.write(ml_doc)
    
    # Example 3: Company Handbook
    handbook_doc = """TechCorp Employee Handbook

Welcome to TechCorp!
We're excited to have you join our team. This handbook provides essential information about our company policies, benefits, and culture.

Company Overview
Founded in 2010, TechCorp is a leading software development company specializing in cloud solutions and AI applications. We serve over 500 enterprise clients worldwide and employ 1,200 talented professionals across 15 offices.

Our Mission
To empower businesses through innovative technology solutions that drive growth and efficiency.

Core Values
1. Innovation: We embrace creativity and encourage bold ideas
2. Integrity: We conduct business ethically and transparently
3. Collaboration: We believe in teamwork and open communication
4. Excellence: We strive for quality in everything we do
5. Inclusivity: We celebrate diversity and create belonging

Work Schedule and Flexibility

Standard Hours: 9:00 AM - 5:00 PM, Monday through Friday
Flexible Work: Employees can adjust start/end times with manager approval
Remote Work: Available 2-3 days per week depending on role
Core Hours: All employees should be available 10:00 AM - 3:00 PM for meetings

Compensation and Benefits

Salary: Competitive market-rate compensation with annual reviews
Health Insurance: Comprehensive medical, dental, and vision coverage
- Company pays 80% of premiums for employees
- Company pays 50% of premiums for dependents

Retirement: 401(k) plan with 5% company match
Stock Options: Eligible employees receive equity grants
Bonuses: Performance-based annual bonuses up to 20% of salary

Time Off Policies

Vacation: 20 days per year (increases with tenure)
Sick Leave: 10 days per year (unused days roll over)
Holidays: 12 paid holidays including major US holidays
Parental Leave: 16 weeks paid leave for primary caregivers, 8 weeks for secondary
Sabbatical: 4-week paid sabbatical after 5 years of service

Professional Development

Training Budget: $2,000 per year for courses, conferences, and certifications
Conference Attendance: Company-sponsored attendance at 1-2 major conferences annually
Internal Learning: Weekly lunch-and-learn sessions and mentorship programs
Tuition Reimbursement: Up to $5,000 per year for degree programs

Office Perks

Free Meals: Catered lunch daily, snacks and beverages always available
Gym Membership: Subsidized memberships to local fitness centers
Transit Benefits: Pre-tax commuter benefits up to $300/month
Ergonomic Equipment: Standing desks, ergonomic chairs, and accessories provided
Game Room: Pool table, ping pong, and video games for breaks

Performance Reviews
Employees receive formal reviews twice annually in June and December. Reviews assess goal achievement, competencies, and development areas. Salary adjustments and promotions are typically announced in January.

Code of Conduct

Respect: Treat all colleagues, clients, and partners with respect and dignity
Confidentiality: Protect company and client information
Conflicts of Interest: Disclose any potential conflicts to management
Harassment: Zero tolerance for harassment or discrimination of any kind
Safety: Follow all health and safety protocols

Technology Policies

Equipment: Company-issued laptop and necessary peripherals
Security: Use strong passwords, enable two-factor authentication, encrypt devices
Data Protection: Follow data handling procedures for client and company information
Personal Use: Reasonable personal use of company technology is permitted
BYOD: Personal devices can access company email with proper security configuration

Communication Channels

Email: Primary business communication
Slack: Team collaboration and quick questions
Zoom: Video conferencing for remote meetings
Weekly All-Hands: Company-wide meeting every Friday at 4:00 PM

Reporting Issues

Direct Manager: First point of contact for most issues
HR Department: hr@techcorp.com or ext. 5000
Ethics Hotline: Anonymous reporting at 1-800-XXX-XXXX
Open Door Policy: Leadership welcomes direct communication

Termination Policies

Resignation: Provide 2 weeks notice when possible
Severance: Eligible employees receive 2 weeks pay per year of service
Exit Interview: Conducted by HR to gather feedback
Equipment Return: All company property must be returned

Contact Information

HR Department: Building A, 3rd Floor
Phone: (555) 123-4567
Email: hr@techcorp.com
Office Hours: Monday-Friday, 8:00 AM - 6:00 PM

We hope you have a rewarding career at TechCorp. Welcome aboard!"""

    with open("employee_handbook.txt", "w", encoding="utf-8") as f:
        f.write(handbook_doc)
    
    print("✅ Created example documents:")
    print("   📄 climate_change.txt - Climate change overview")
    print("   📄 machine_learning.txt - ML beginner's guide")
    print("   📄 employee_handbook.txt - Company policies")
    print("\n💡 Use these to test the Q&A system!")
    print("   Example: python document_qa.py climate_change.txt")


if __name__ == "__main__":
    create_example_documents()