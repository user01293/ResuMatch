"""
Curated job descriptions dataset covering 30+ roles across major industries.
Data inspired by real job postings from LinkedIn, Glassdoor, and Indeed.
"""

JOBS_DATASET = [
    {
        "id": 1,
        "title": "Software Engineer",
        "company": "TechCorp Solutions",
        "location": "San Francisco, CA",
        "type": "Full-time",
        "salary": "$120,000 - $160,000",
        "category": "Engineering",
        "description": """
        We are looking for a skilled Software Engineer to join our team.
        You will design, develop, and maintain software applications using Python, Java, or JavaScript.
        Responsibilities include writing clean, scalable code, participating in code reviews,
        collaborating with cross-functional teams, and deploying applications to cloud platforms.
        """,
        "skills": ["Python", "Java", "JavaScript", "REST APIs", "Git", "SQL", "Agile", "AWS", "Docker", "Linux"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science or related field"
    },
    {
        "id": 2,
        "title": "Data Scientist",
        "company": "Analytics Pro",
        "location": "New York, NY",
        "type": "Full-time",
        "salary": "$130,000 - $170,000",
        "category": "Data & Analytics",
        "description": """
        Seeking an experienced Data Scientist to analyze large datasets and build predictive models.
        You will work with machine learning algorithms, statistical modeling, and data visualization.
        Experience with Python, R, TensorFlow, PyTorch, and SQL databases is required.
        You will collaborate with business stakeholders to translate data insights into actionable strategies.
        """,
        "skills": ["Python", "R", "Machine Learning", "TensorFlow", "PyTorch", "SQL", "Statistics", "Data Visualization", "Pandas", "NumPy", "Scikit-learn"],
        "experience": "3-5 years",
        "education": "M.S. or Ph.D. in Data Science, Statistics, or related field"
    },
    {
        "id": 3,
        "title": "Frontend Developer",
        "company": "Creative Web Agency",
        "location": "Austin, TX",
        "type": "Full-time",
        "salary": "$90,000 - $130,000",
        "category": "Engineering",
        "description": """
        We need a talented Frontend Developer to build beautiful, responsive web applications.
        You will work with React, Vue.js, or Angular frameworks to create intuitive user interfaces.
        Strong HTML5, CSS3, JavaScript ES6+ skills required. Experience with TypeScript, Webpack,
        and modern build tools preferred. You will work closely with UI/UX designers.
        """,
        "skills": ["React", "Vue.js", "Angular", "JavaScript", "TypeScript", "HTML5", "CSS3", "Webpack", "Git", "REST APIs", "Redux"],
        "experience": "2-4 years",
        "education": "B.S. in Computer Science or equivalent experience"
    },
    {
        "id": 4,
        "title": "Machine Learning Engineer",
        "company": "AI Innovations Inc",
        "location": "Seattle, WA",
        "type": "Full-time",
        "salary": "$150,000 - $200,000",
        "category": "AI/ML",
        "description": """
        Join our ML team to build and deploy production machine learning systems at scale.
        You will design ML pipelines, optimize model performance, and implement MLOps practices.
        Strong background in deep learning, NLP, computer vision, or recommendation systems.
        Experience with TensorFlow, PyTorch, Kubernetes, and cloud ML platforms (AWS SageMaker, GCP Vertex AI).
        """,
        "skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "NLP", "MLOps", "Kubernetes", "AWS SageMaker", "Docker", "Spark"],
        "experience": "4-6 years",
        "education": "M.S. or Ph.D. in Computer Science, Machine Learning, or related"
    },
    {
        "id": 5,
        "title": "DevOps Engineer",
        "company": "CloudBase Technologies",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$110,000 - $150,000",
        "category": "Engineering",
        "description": """
        We are looking for a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines.
        You will automate deployments, monitor system performance, and ensure high availability.
        Strong experience with AWS, Azure, or GCP, Terraform, Ansible, Docker, and Kubernetes required.
        Linux system administration and scripting with Bash and Python are essential.
        """,
        "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "CI/CD", "Jenkins", "Linux", "Python", "Bash", "Monitoring"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science or related field"
    },
    {
        "id": 6,
        "title": "Product Manager",
        "company": "ProductFirst Corp",
        "location": "San Francisco, CA",
        "type": "Full-time",
        "salary": "$130,000 - $175,000",
        "category": "Product",
        "description": """
        We need a strategic Product Manager to drive product vision and roadmap.
        You will gather requirements from customers, prioritize features, and work with engineering teams.
        Strong analytical skills, experience with product metrics, A/B testing, and user research required.
        Excellent communication skills to present to executives and stakeholders.
        """,
        "skills": ["Product Strategy", "Agile", "Scrum", "User Research", "A/B Testing", "Analytics", "Roadmapping", "JIRA", "Stakeholder Management", "Data Analysis"],
        "experience": "4-6 years",
        "education": "B.S. in Business, Computer Science, or related; MBA preferred"
    },
    {
        "id": 7,
        "title": "UX/UI Designer",
        "company": "Design Studio X",
        "location": "New York, NY",
        "type": "Full-time",
        "salary": "$90,000 - $130,000",
        "category": "Design",
        "description": """
        Join our design team to create exceptional user experiences for web and mobile products.
        You will conduct user research, create wireframes, prototypes, and high-fidelity mockups.
        Proficiency in Figma, Sketch, Adobe XD required. Experience with design systems,
        accessibility standards, and usability testing is essential. Strong portfolio required.
        """,
        "skills": ["Figma", "Sketch", "Adobe XD", "User Research", "Wireframing", "Prototyping", "Design Systems", "Usability Testing", "CSS", "HTML", "Adobe Creative Suite"],
        "experience": "3-5 years",
        "education": "B.S. in Design, HCI, or related field"
    },
    {
        "id": 8,
        "title": "Cybersecurity Analyst",
        "company": "SecureShield Corp",
        "location": "Washington, DC",
        "type": "Full-time",
        "salary": "$100,000 - $140,000",
        "category": "Security",
        "description": """
        Protect our organization's digital assets as a Cybersecurity Analyst.
        Responsibilities include monitoring security systems, conducting vulnerability assessments,
        incident response, and implementing security controls. Experience with SIEM tools,
        penetration testing, network security, and compliance frameworks (SOC2, ISO 27001, NIST).
        """,
        "skills": ["Network Security", "SIEM", "Penetration Testing", "Vulnerability Assessment", "Incident Response", "Firewall", "Python", "Linux", "SOC2", "NIST", "CISSP"],
        "experience": "3-5 years",
        "education": "B.S. in Cybersecurity, Computer Science; CISSP or CEH certification preferred"
    },
    {
        "id": 9,
        "title": "Cloud Architect",
        "company": "Enterprise Cloud Co",
        "location": "Chicago, IL",
        "type": "Full-time",
        "salary": "$160,000 - $220,000",
        "category": "Engineering",
        "description": """
        Lead our cloud transformation as a Cloud Architect designing scalable, secure cloud solutions.
        You will define cloud strategy, design multi-cloud architectures, and guide migration projects.
        Deep expertise in AWS, Azure, or GCP, microservices, serverless computing, and cost optimization.
        Experience with enterprise architecture frameworks and leading technical teams required.
        """,
        "skills": ["AWS", "Azure", "GCP", "Microservices", "Serverless", "Architecture Design", "Terraform", "Kubernetes", "Security", "Cost Optimization", "Python", "Leadership"],
        "experience": "7+ years",
        "education": "B.S. in Computer Science; AWS/Azure/GCP certifications required"
    },
    {
        "id": 10,
        "title": "Data Engineer",
        "company": "DataFlow Systems",
        "location": "Boston, MA",
        "type": "Full-time",
        "salary": "$120,000 - $160,000",
        "category": "Data & Analytics",
        "description": """
        Build robust data pipelines and infrastructure as a Data Engineer.
        You will design ETL processes, maintain data warehouses, and optimize query performance.
        Strong experience with Apache Spark, Kafka, Airflow, dbt, and cloud data platforms
        (Snowflake, BigQuery, Redshift). Python and SQL expertise essential.
        """,
        "skills": ["Python", "SQL", "Apache Spark", "Kafka", "Airflow", "dbt", "Snowflake", "BigQuery", "Redshift", "ETL", "Data Warehousing", "AWS"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science, Engineering, or related field"
    },
    {
        "id": 11,
        "title": "Full Stack Developer",
        "company": "Startup Ventures",
        "location": "Denver, CO",
        "type": "Full-time",
        "salary": "$100,000 - $145,000",
        "category": "Engineering",
        "description": """
        We need a versatile Full Stack Developer comfortable with both frontend and backend development.
        Build features across our entire technology stack using React, Node.js, Python, and PostgreSQL.
        Experience with microservices, REST and GraphQL APIs, cloud deployments, and Agile methodologies.
        Ability to take ownership of features from design to deployment.
        """,
        "skills": ["React", "Node.js", "Python", "JavaScript", "PostgreSQL", "MongoDB", "REST APIs", "GraphQL", "Docker", "AWS", "Git", "Agile"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science or equivalent"
    },
    {
        "id": 12,
        "title": "Business Analyst",
        "company": "Consulting Dynamics",
        "location": "Atlanta, GA",
        "type": "Full-time",
        "salary": "$80,000 - $110,000",
        "category": "Business",
        "description": """
        Seeking a Business Analyst to bridge the gap between business needs and technology solutions.
        You will gather requirements, document processes, analyze data, and present findings to stakeholders.
        Experience with SQL, Excel, Tableau or Power BI, and JIRA required.
        Knowledge of Agile/Scrum methodologies and business process modeling preferred.
        """,
        "skills": ["Business Analysis", "SQL", "Excel", "Tableau", "Power BI", "Requirements Gathering", "Process Modeling", "JIRA", "Agile", "Communication", "Stakeholder Management"],
        "experience": "2-4 years",
        "education": "B.S. in Business Administration, Information Systems, or related"
    },
    {
        "id": 13,
        "title": "Marketing Manager",
        "company": "Growth Marketing Co",
        "location": "Los Angeles, CA",
        "type": "Full-time",
        "salary": "$85,000 - $120,000",
        "category": "Marketing",
        "description": """
        Lead our marketing initiatives as a Marketing Manager driving brand growth and customer acquisition.
        Experience with digital marketing, SEO/SEM, social media, content marketing, and email campaigns.
        Strong analytical skills with Google Analytics, HubSpot, or Salesforce.
        Ability to manage marketing budgets, campaigns, and a small team of marketers.
        """,
        "skills": ["Digital Marketing", "SEO", "SEM", "Social Media", "Content Marketing", "Google Analytics", "HubSpot", "Email Marketing", "Campaign Management", "Budget Management", "Leadership"],
        "experience": "4-6 years",
        "education": "B.S. in Marketing, Business, or related field"
    },
    {
        "id": 14,
        "title": "Financial Analyst",
        "company": "Capital Group",
        "location": "New York, NY",
        "type": "Full-time",
        "salary": "$90,000 - $130,000",
        "category": "Finance",
        "description": """
        Join our finance team as a Financial Analyst performing financial modeling and analysis.
        You will prepare financial reports, conduct variance analysis, forecast revenue, and support
        investment decisions. Advanced Excel, SQL, and financial modeling skills required.
        Experience with Bloomberg, Tableau, and ERP systems (SAP, Oracle) preferred.
        """,
        "skills": ["Financial Modeling", "Excel", "SQL", "Financial Analysis", "Forecasting", "Bloomberg", "SAP", "Tableau", "Budgeting", "Accounting", "CFA"],
        "experience": "2-4 years",
        "education": "B.S. in Finance, Accounting, or Economics; CFA preferred"
    },
    {
        "id": 15,
        "title": "HR Manager",
        "company": "People First Inc",
        "location": "Dallas, TX",
        "type": "Full-time",
        "salary": "$80,000 - $110,000",
        "category": "Human Resources",
        "description": """
        Lead HR operations and talent management as an HR Manager.
        Responsibilities include recruitment, onboarding, performance management, employee relations,
        and HR compliance. Experience with HRIS systems (Workday, ADP), employment law,
        and developing HR policies and programs. Strong interpersonal and communication skills.
        """,
        "skills": ["Recruitment", "Talent Management", "Workday", "ADP", "Employee Relations", "Performance Management", "HR Compliance", "Onboarding", "Training", "Communication", "Leadership"],
        "experience": "5-7 years",
        "education": "B.S. in Human Resources, Business; PHR or SHRM-CP certification preferred"
    },
    {
        "id": 16,
        "title": "Backend Developer",
        "company": "API Masters",
        "location": "Portland, OR",
        "type": "Full-time",
        "salary": "$105,000 - $145,000",
        "category": "Engineering",
        "description": """
        Build powerful backend systems and APIs as a Backend Developer.
        Strong experience with Python (Django/FastAPI), Java (Spring Boot), or Node.js.
        Design RESTful and GraphQL APIs, work with PostgreSQL and Redis, implement microservices.
        Experience with message queues (RabbitMQ, Kafka), caching strategies, and performance optimization.
        """,
        "skills": ["Python", "Django", "FastAPI", "Java", "Spring Boot", "Node.js", "PostgreSQL", "Redis", "REST APIs", "GraphQL", "Microservices", "Kafka", "Docker"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science or related"
    },
    {
        "id": 17,
        "title": "Mobile Developer (iOS/Android)",
        "company": "AppWorks Studio",
        "location": "Miami, FL",
        "type": "Full-time",
        "salary": "$110,000 - $150,000",
        "category": "Engineering",
        "description": """
        Build world-class mobile applications as a Mobile Developer.
        Experience with Swift/SwiftUI for iOS or Kotlin/Jetpack Compose for Android.
        Cross-platform experience with React Native or Flutter is a plus.
        Knowledge of mobile app architecture, App Store/Play Store deployment, and performance optimization.
        """,
        "skills": ["Swift", "iOS", "Kotlin", "Android", "React Native", "Flutter", "SwiftUI", "Jetpack Compose", "REST APIs", "Git", "Mobile Architecture", "Xcode"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science or equivalent"
    },
    {
        "id": 18,
        "title": "Blockchain Developer",
        "company": "Web3 Ventures",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$140,000 - $200,000",
        "category": "Engineering",
        "description": """
        Build decentralized applications and smart contracts as a Blockchain Developer.
        Strong experience with Solidity, Ethereum, and Web3.js or Ethers.js.
        Knowledge of DeFi protocols, NFT standards (ERC-721, ERC-1155), and Layer 2 solutions.
        Experience with Hardhat, Truffle, and IPFS. Rust experience for Solana is a plus.
        """,
        "skills": ["Solidity", "Ethereum", "Web3.js", "Ethers.js", "Smart Contracts", "DeFi", "NFT", "Hardhat", "Truffle", "IPFS", "JavaScript", "Python", "Rust"],
        "experience": "2-5 years",
        "education": "B.S. in Computer Science or equivalent experience"
    },
    {
        "id": 19,
        "title": "Site Reliability Engineer (SRE)",
        "company": "Reliability Systems",
        "location": "San Jose, CA",
        "type": "Full-time",
        "salary": "$130,000 - $180,000",
        "category": "Engineering",
        "description": """
        Ensure reliability and performance of large-scale distributed systems as an SRE.
        You will implement SLOs/SLIs, build monitoring solutions, and handle incident management.
        Strong software engineering skills combined with deep systems knowledge.
        Experience with Prometheus, Grafana, PagerDuty, Kubernetes, and cloud platforms.
        """,
        "skills": ["Linux", "Python", "Go", "Kubernetes", "Prometheus", "Grafana", "AWS", "Distributed Systems", "Incident Management", "CI/CD", "Automation", "SRE"],
        "experience": "4-6 years",
        "education": "B.S. in Computer Science or related"
    },
    {
        "id": 20,
        "title": "QA Engineer",
        "company": "Quality Tech Solutions",
        "location": "Phoenix, AZ",
        "type": "Full-time",
        "salary": "$80,000 - $115,000",
        "category": "Engineering",
        "description": """
        Ensure software quality as a QA Engineer building comprehensive test strategies.
        Experience with test automation frameworks (Selenium, Cypress, Playwright, Appium).
        Write test plans, execute manual and automated testing, API testing with Postman.
        Experience with CI/CD pipelines, performance testing (JMeter), and bug tracking.
        """,
        "skills": ["Selenium", "Cypress", "Playwright", "Test Automation", "Python", "JavaScript", "API Testing", "Postman", "JMeter", "JIRA", "Agile", "CI/CD"],
        "experience": "2-4 years",
        "education": "B.S. in Computer Science or related field"
    },
    {
        "id": 21,
        "title": "AI Research Scientist",
        "company": "DeepMind Labs",
        "location": "Cambridge, MA",
        "type": "Full-time",
        "salary": "$180,000 - $280,000",
        "category": "AI/ML",
        "description": """
        Conduct cutting-edge AI research and publish results as an AI Research Scientist.
        Focus areas include large language models, reinforcement learning, computer vision, or AI safety.
        Strong publication record in top-tier venues (NeurIPS, ICML, ICLR, CVPR).
        Deep expertise in PyTorch or JAX, distributed training, and large-scale experiments.
        """,
        "skills": ["Python", "PyTorch", "JAX", "Deep Learning", "NLP", "LLM", "Reinforcement Learning", "Computer Vision", "Research", "Mathematics", "Statistics", "CUDA"],
        "experience": "PhD + 2 years",
        "education": "Ph.D. in Computer Science, Machine Learning, or Mathematics"
    },
    {
        "id": 22,
        "title": "Sales Engineer",
        "company": "Enterprise Solutions",
        "location": "Chicago, IL",
        "type": "Full-time",
        "salary": "$100,000 - $140,000",
        "category": "Sales",
        "description": """
        Bridge the gap between sales and engineering as a Sales Engineer.
        Conduct technical product demonstrations, answer technical questions from prospects,
        and create proof-of-concept solutions. Strong communication and presentation skills.
        Technical background in software, cloud, or data products required with CRM experience.
        """,
        "skills": ["Technical Sales", "Product Demonstrations", "Communication", "Salesforce", "CRM", "Cloud", "API Integration", "Python", "SQL", "Presentation", "Solution Architecture"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science, Engineering, or Business"
    },
    {
        "id": 23,
        "title": "Database Administrator",
        "company": "DataBase Corp",
        "location": "Houston, TX",
        "type": "Full-time",
        "salary": "$95,000 - $130,000",
        "category": "Data & Analytics",
        "description": """
        Manage and optimize database systems as a Database Administrator.
        Expertise in PostgreSQL, MySQL, Oracle, or SQL Server required.
        Responsibilities include performance tuning, backup/recovery, replication, and security.
        Experience with NoSQL databases (MongoDB, Cassandra, Redis) and cloud databases is a plus.
        """,
        "skills": ["PostgreSQL", "MySQL", "Oracle", "SQL Server", "MongoDB", "Redis", "Performance Tuning", "Backup Recovery", "Replication", "SQL", "Linux", "AWS RDS"],
        "experience": "4-6 years",
        "education": "B.S. in Computer Science or Information Systems"
    },
    {
        "id": 24,
        "title": "Content Writer / Technical Writer",
        "company": "Content Hub",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$65,000 - $90,000",
        "category": "Marketing",
        "description": """
        Create compelling content and technical documentation as a Content/Technical Writer.
        Write blog posts, API documentation, user guides, whitepapers, and case studies.
        Strong writing, editing, and research skills. Familiarity with developer tools, APIs, or SaaS products.
        Experience with Markdown, Confluence, and content management systems.
        """,
        "skills": ["Technical Writing", "Content Writing", "Markdown", "Confluence", "SEO", "API Documentation", "Research", "Editing", "CMS", "Communication", "Git"],
        "experience": "2-4 years",
        "education": "B.S. in English, Communication, Computer Science, or related"
    },
    {
        "id": 25,
        "title": "Scrum Master / Agile Coach",
        "company": "Agile Experts",
        "location": "Minneapolis, MN",
        "type": "Full-time",
        "salary": "$95,000 - $130,000",
        "category": "Product",
        "description": """
        Facilitate Agile practices and coach teams as a Scrum Master.
        Lead sprint ceremonies, remove blockers, and improve team performance.
        CSM or PSM certification required. Experience scaling Agile with SAFe or LeSS frameworks.
        Strong facilitation, coaching, and conflict resolution skills with experience in JIRA and Confluence.
        """,
        "skills": ["Scrum", "Agile", "Coaching", "JIRA", "Confluence", "SAFe", "Sprint Planning", "Facilitation", "Kanban", "Retrospectives", "Conflict Resolution", "CSM"],
        "experience": "3-5 years",
        "education": "B.S. in any field; CSM/PSM certification required"
    },
    {
        "id": 26,
        "title": "Network Engineer",
        "company": "NetSystems Corp",
        "location": "Columbus, OH",
        "type": "Full-time",
        "salary": "$90,000 - $125,000",
        "category": "Engineering",
        "description": """
        Design and maintain enterprise network infrastructure as a Network Engineer.
        Experience with Cisco, Juniper, or Palo Alto networking equipment.
        Strong knowledge of TCP/IP, BGP, OSPF, VLANs, SD-WAN, and network security.
        Experience with network monitoring tools and automation using Python or Ansible.
        """,
        "skills": ["Cisco", "TCP/IP", "BGP", "OSPF", "VLANs", "SD-WAN", "Network Security", "Juniper", "Python", "Ansible", "Linux", "Firewall", "CCNA"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science or Networking; CCNA/CCNP preferred"
    },
    {
        "id": 27,
        "title": "Embedded Systems Engineer",
        "company": "IoT Solutions Ltd",
        "location": "San Diego, CA",
        "type": "Full-time",
        "salary": "$110,000 - $150,000",
        "category": "Engineering",
        "description": """
        Develop firmware and embedded software for IoT devices as an Embedded Systems Engineer.
        Strong C/C++ programming skills for embedded systems required.
        Experience with microcontrollers (ARM Cortex, STM32), RTOS, communication protocols (I2C, SPI, UART, CAN).
        Knowledge of PCB design, hardware debugging, and low-power design techniques.
        """,
        "skills": ["C", "C++", "Embedded Systems", "ARM", "RTOS", "I2C", "SPI", "UART", "CAN", "IoT", "Firmware", "Linux", "Python", "Hardware Debugging"],
        "experience": "3-6 years",
        "education": "B.S. in Electrical Engineering, Computer Engineering, or related"
    },
    {
        "id": 28,
        "title": "Project Manager",
        "company": "Project Solutions Inc",
        "location": "Nashville, TN",
        "type": "Full-time",
        "salary": "$90,000 - $125,000",
        "category": "Product",
        "description": """
        Manage technology projects from inception to completion as a Project Manager.
        PMP certification preferred. Experience managing software development projects using Agile and Waterfall.
        Strong stakeholder management, risk assessment, and budget management skills.
        Proficiency with project management tools (MS Project, Asana, Monday.com, JIRA).
        """,
        "skills": ["Project Management", "PMP", "Agile", "Waterfall", "Stakeholder Management", "Risk Management", "Budget Management", "JIRA", "Asana", "MS Project", "Communication"],
        "experience": "5-7 years",
        "education": "B.S. in Business, Engineering, or IT; PMP certification preferred"
    },
    {
        "id": 29,
        "title": "Data Analyst",
        "company": "Insight Analytics",
        "location": "Philadelphia, PA",
        "type": "Full-time",
        "salary": "$75,000 - $105,000",
        "category": "Data & Analytics",
        "description": """
        Transform raw data into meaningful insights as a Data Analyst.
        Strong SQL skills and experience with BI tools (Tableau, Power BI, Looker) required.
        Proficiency in Python or R for data analysis and visualization.
        Experience with Excel, statistical analysis, and presenting findings to non-technical audiences.
        """,
        "skills": ["SQL", "Tableau", "Power BI", "Python", "R", "Excel", "Data Visualization", "Statistics", "Looker", "Google Analytics", "ETL", "Communication"],
        "experience": "1-3 years",
        "education": "B.S. in Statistics, Mathematics, Computer Science, or related"
    },
    {
        "id": 30,
        "title": "Game Developer",
        "company": "GameStudio Pro",
        "location": "Redmond, WA",
        "type": "Full-time",
        "salary": "$100,000 - $145,000",
        "category": "Engineering",
        "description": """
        Create engaging gaming experiences as a Game Developer.
        Strong experience with Unity (C#) or Unreal Engine (C++/Blueprints) required.
        Knowledge of game physics, rendering pipelines, multiplayer networking, and shader programming.
        Experience with 3D math, animation systems, and optimizing for mobile or console platforms.
        """,
        "skills": ["Unity", "Unreal Engine", "C#", "C++", "Game Development", "3D Math", "Shader Programming", "Multiplayer", "Physics", "Animation", "Mobile Gaming", "OpenGL"],
        "experience": "3-5 years",
        "education": "B.S. in Computer Science or Game Development"
    },
    {
        "id": 31,
        "title": "NLP Engineer",
        "company": "Language AI Corp",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$140,000 - $190,000",
        "category": "AI/ML",
        "description": """
        Build natural language processing systems as an NLP Engineer.
        Deep expertise in transformer models, BERT, GPT, and large language models.
        Experience fine-tuning LLMs, building RAG systems, and deploying NLP at scale.
        Strong Python skills with Hugging Face Transformers, LangChain, and vector databases.
        """,
        "skills": ["Python", "NLP", "BERT", "GPT", "LLM", "Transformers", "Hugging Face", "LangChain", "RAG", "Vector Databases", "PyTorch", "Fine-tuning", "Embeddings"],
        "experience": "3-5 years",
        "education": "M.S. or Ph.D. in Computer Science, Linguistics, or related"
    },
    {
        "id": 32,
        "title": "Solutions Architect",
        "company": "Enterprise Architecture Group",
        "location": "Boston, MA",
        "type": "Full-time",
        "salary": "$150,000 - $210,000",
        "category": "Engineering",
        "description": """
        Design enterprise-grade solutions as a Solutions Architect for our clients.
        Deep knowledge of cloud architectures, integration patterns, and enterprise systems.
        Experience with AWS/Azure/GCP, microservices, event-driven architectures, and API design.
        Strong communication skills to present technical solutions to C-level executives.
        """,
        "skills": ["AWS", "Azure", "Architecture Design", "Microservices", "API Design", "System Design", "Cloud", "Python", "Java", "Integration", "Communication", "Leadership"],
        "experience": "8+ years",
        "education": "B.S. in Computer Science or Engineering; Cloud certifications required"
    }
]
