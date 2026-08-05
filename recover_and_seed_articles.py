import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.articles.models import Article, Category, Tag
from apps.users.models import CustomUser
from django.utils import timezone
from django.core.management import call_command

# 1. Ensure categories are seeded
call_command('seed_categories')

# 2. Retrieve or create author user
author = CustomUser.objects.filter(is_superuser=True).first()
if not author:
    author = CustomUser.objects.filter(is_staff=True).first()
if not author:
    author = CustomUser.objects.first()
if not author:
    author = CustomUser.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="Password123!",
        is_staff=True,
        is_superuser=True,
    )

print(f"Using author: {author.username} ({author.email})")

articles_data = [
    {
        "id": "68efd5f94f9d422bb3d5ff4cd1b4377a",
        "title": "The Rise of Artificial Intelligence: Transforming the Future of Technology",
        "slug": "the-rise-of-artificial-intelligence-transforming-the-future-of-technology",
        "category_slug": "ai",
        "excerpt": "Artificial Intelligence (AI) is revolutionizing industries worldwide by automating tasks, enhancing decision-making, and enabling smarter applications. Explore how AI is shaping the future of technology and everyday life.",
        "content": """<h2>Introduction</h2>
<p>
Artificial Intelligence (AI) is one of the most transformative technologies of the 21st century. From powering virtual assistants to enabling self-driving cars, AI is reshaping how we interact with technology and the world around us.
</p>

<h2>What is Artificial Intelligence?</h2>
<p>
Artificial Intelligence refers to the simulation of human intelligence in machines that are programmed to think, learn, and make decisions. It includes technologies like Machine Learning, Natural Language Processing (NLP), and Computer Vision.
</p>

<h2>Key Applications of AI</h2>
<ul>
  <li><strong>Healthcare:</strong> AI helps in disease detection, medical imaging, and personalized treatment.</li>
  <li><strong>Finance:</strong> Fraud detection, algorithmic trading, and risk assessment are powered by AI.</li>
  <li><strong>E-commerce:</strong> Personalized recommendations and chatbots improve user experience.</li>
  <li><strong>Education:</strong> AI enables adaptive learning and smart content delivery.</li>
</ul>

<h2>Benefits of AI</h2>
<p>
AI offers numerous advantages including automation of repetitive tasks, improved accuracy, faster decision-making, and enhanced productivity. Businesses leverage AI to gain insights from data and stay competitive.
</p>

<h2>Challenges and Concerns</h2>
<p>
Despite its benefits, AI also raises concerns such as data privacy, job displacement, and ethical issues. It is important to develop AI responsibly to ensure it benefits society as a whole.
</p>

<h2>The Future of AI</h2>
<p>
The future of AI is promising, with advancements in deep learning, robotics, and automation. AI will continue to evolve and become more integrated into our daily lives, driving innovation across industries.
</p>

<h2>Conclusion</h2>
<p>
Artificial Intelligence is not just a trend—it is a fundamental shift in how technology works. As AI continues to grow, it will unlock new possibilities and redefine the future of human potential.
</p>""",
        "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
        "status": Article.STATUS_PUBLISHED,
        "is_featured": True,
        "tag_names": ["Machine Learning", "Deep Learning", "Artificial Intelligence"],
    },
    {
        "id": "55f9f7723be64027b24f9b5b82740b18",
        "title": "The Future of Artificial Intelligence: Opportunities, Challenges, and Global Impact",
        "slug": "the-future-of-artificial-intelligence-opportunities-challenges-and-global-impact",
        "category_slug": "ai",
        "excerpt": "Artificial Intelligence is transforming how we work, think, and innovate. From automation to advanced decision-making, AI is shaping the future across industries and societies worldwide.",
        "content": """<h3>Introduction</h3><p>Artificial Intelligence (AI) has become one of the most powerful forces driving innovation in the modern world. From smart assistants to advanced data analytics, AI is transforming how individuals, businesses, and societies function. It enables machines to learn, adapt, and make decisions, opening new possibilities across multiple domains.</p><hr><h3>What is Artificial Intelligence?</h3><p>Artificial Intelligence refers to the ability of machines to simulate human intelligence. It includes technologies such as machine learning, natural language processing, and computer vision. These systems are designed to analyze data, recognize patterns, and make predictions or decisions with minimal human intervention.</p><hr><h3>Key Applications of AI</h3><ul><li><p><strong>Healthcare:</strong> AI helps in diagnosing diseases, analyzing medical images, and providing personalized treatment recommendations.</p></li><li><p><strong>Business:</strong> Companies use AI for customer insights, automation, and improving operational efficiency.</p></li><li><p><strong>Education:</strong> AI-powered tools provide personalized learning experiences and smart tutoring systems.</p></li><li><p><strong>Technology:</strong> AI drives innovations like chatbots, recommendation systems, and autonomous vehicles.</p></li></ul><hr><h3>Benefits of Artificial Intelligence</h3><p>Artificial Intelligence offers several advantages that make it a valuable technology for the future. It increases efficiency, reduces human error, and enables faster decision-making. Businesses can automate repetitive tasks, while researchers can analyze large datasets quickly and accurately.</p><ul><li><p>Improves productivity and efficiency</p></li><li><p>Enhances accuracy and reduces errors</p></li><li><p>Enables data-driven decision making</p></li><li><p>Automates repetitive and time-consuming tasks</p></li></ul><hr><h3>Challenges and Concerns</h3><p>Despite its benefits, AI also brings challenges. Issues such as data privacy, algorithm bias, and job displacement need careful consideration. Ensuring ethical use of AI is essential to avoid misuse and maintain trust in technology.</p><hr><h3>The Future of AI</h3><p>The future of Artificial Intelligence is promising and full of opportunities. As AI continues to evolve, it will become more integrated into everyday life. From smart cities to advanced healthcare systems, AI will play a critical role in shaping a smarter and more connected world.</p><hr><h3>Conclusion</h3><p>Artificial Intelligence is not just a technological advancement—it is a transformation that is redefining the future. By embracing AI responsibly and innovatively, we can unlock its full potential and create meaningful impact across industries and societies.</p>""",
        "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
        "status": Article.STATUS_PUBLISHED,
        "is_featured": False,
        "tag_names": ["Machine Learning", "Deep Learning"],
    },
    {
        "title": "Modern Software Architecture: Building Resilient Distributed Systems",
        "slug": "modern-software-architecture-building-resilient-distributed-systems",
        "category_slug": "software-development",
        "excerpt": "Discover modern architectural patterns for building fault-tolerant, high-performance microservices and cloud-native application platforms.",
        "content": """<h2>Introduction to Cloud-Native Architecture</h2>
<p>Modern software development requires systems that can scale seamlessly, handle high throughput, and recover automatically from failure. Microservices and domain-driven design are at the core of this engineering paradigm.</p>
<h2>Key Architectural Pillars</h2>
<ul>
  <li><strong>Decoupled Microservices:</strong> Isolate domains to enable independent deployment cycles.</li>
  <li><strong>Event-Driven Communication:</strong> Use message queues like Kafka or RabbitMQ for asynchronous processing.</li>
  <li><strong>Observability:</strong> Integrate distributed tracing, metric dashboards, and structured logging.</li>
</ul>
<h2>Conclusion</h2>
<p>Adopting clean architectural patterns ensures your application remains maintainable and adaptable for decades.</p>""",
        "cover_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c",
        "status": Article.STATUS_PUBLISHED,
        "is_featured": True,
        "tag_names": ["Software Architecture", "Cloud Computing", "Web Development"],
    },
    {
        "title": "Navigating Early-Stage Startup Funding and Growth Strategies",
        "slug": "navigating-early-stage-startup-funding-and-growth-strategies",
        "category_slug": "business-startups",
        "excerpt": "A practical playbook for founders seeking venture capital, bootstrapping efficiently, and achieving sustainable product-market fit.",
        "content": """<h2>Foundations of Early Stage Startups</h2>
<p>Building a successful venture starts with validating real problems for paying customers before scaling operations.</p>
<h2>Funding Avenues</h2>
<ul>
  <li><strong>Bootstrapping:</strong> Retain equity and build initial momentum using self-funded cashflow.</li>
  <li><strong>Angel & Seed Investors:</strong> Partner with strategic advisors who bring network and expertise.</li>
  <li><strong>Venture Capital:</strong> Raise growth capital once unit economics are proven.</li>
</ul>
<h2>Summary</h2>
<p>Focus relentlessly on retention and customer satisfaction to drive exponential growth.</p>""",
        "cover_image": "https://images.unsplash.com/photo-1559136555-9303baea8ebd",
        "status": Article.STATUS_PUBLISHED,
        "is_featured": False,
        "tag_names": ["Startups", "Venture Capital", "Product Strategy"],
    },
    {
        "title": "Cybersecurity in the Era of Advanced Threat Vectors",
        "slug": "cybersecurity-in-the-era-of-advanced-threat-vectors",
        "category_slug": "cybersecurity",
        "excerpt": "Key strategies for zero-trust security architecture, automated incident response, and proactive digital threat mitigation.",
        "content": """<h2>The Shifting Threat Landscape</h2>
<p>As cyber threats evolve, organizations must transition from perimeter defense to zero-trust architecture.</p>
<h2>Core Defense Mechanisms</h2>
<ul>
  <li><strong>Zero Trust Architecture:</strong> Always verify, never trust.</li>
  <li><strong>Automated Anomaly Detection:</strong> Monitor network telemetry in real-time.</li>
  <li><strong>Data Encryption:</strong> Protect sensitive assets at rest and in transit.</li>
</ul>""",
        "cover_image": "https://images.unsplash.com/photo-1563986768609-322da13575f3",
        "status": Article.STATUS_PUBLISHED,
        "is_featured": True,
        "tag_names": ["Cybersecurity", "Software Architecture"],
    },
    {
        "title": "The Frontiers of Data Science: Big Data to Actionable Intelligence",
        "slug": "the-frontiers-of-data-science-big-data-to-actionable-intelligence",
        "category_slug": "data-science",
        "excerpt": "How modern data pipelines, feature engineering, and automated machine learning turn vast datasets into real-time business insights.",
        "content": """<h2>Data Engineering at Scale</h2>
<p>Extracting value from petabytes of data requires robust ingestion pipelines, data lakes, and continuous feature stores.</p>
<h2>Machine Learning Pipelines</h2>
<p>Automated MLOps pipelines ensure models are monitored for drift and continuously retrained on fresh telemetry.</p>""",
        "cover_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
        "status": Article.STATUS_PUBLISHED,
        "is_featured": False,
        "tag_names": ["Data Engineering", "Machine Learning", "Artificial Intelligence"],
    },
    {
        "title": "Biomedical Innovations and the Breakthroughs in Precision Healthcare",
        "slug": "biomedical-innovations-and-the-breakthroughs-in-precision-healthcare",
        "category_slug": "health",
        "excerpt": "How gene editing, AI diagnostics, and targeted therapeutics are extending human healthspan and transforming clinical outcomes.",
        "content": """<h2>Precision Medicine & Diagnostics</h2>
<p>Combining genomic sequencing with machine learning algorithms is enabling earlier disease detection and targeted treatments tailored to individual genetics.</p>""",
        "cover_image": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69",
        "status": Article.STATUS_PUBLISHED,
        "is_featured": False,
        "tag_names": ["Genetics", "Public Health"],
    },
]

for item in articles_data:
    cat = Category.objects.filter(slug=item["category_slug"]).first()
    
    article_kwargs = {
        "title": item["title"],
        "slug": item["slug"],
        "excerpt": item["excerpt"],
        "content": item["content"],
        "cover_image": item["cover_image"],
        "cover_image_thumbnail": item["cover_image"],
        "cover_image_medium": item["cover_image"],
        "cover_image_large": item["cover_image"],
        "status": item["status"],
        "is_featured": item["is_featured"],
        "category": cat,
        "author": author,
        "published_at": timezone.now(),
    }
    
    if "id" in item:
        article_kwargs["id"] = item["id"]

    article, created = Article.objects.update_or_create(
        slug=item["slug"],
        defaults=article_kwargs
    )

    tags = []
    for tag_name in item["tag_names"]:
        slug = tag_name.lower().replace(" ", "-")
        t, _ = Tag.objects.get_or_create(name=tag_name, defaults={"slug": slug})
        tags.append(t)
    
    article.tags.set(tags)
    action = "Created" if created else "Updated"
    print(f"{action} article: {article.title} (Category: {cat.name if cat else 'None'}, Tags: {[t.name for t in tags]})")

print("\n--- Final Summary ---")
print(f"Total Categories: {Category.objects.count()}")
print(f"Total Tags: {Tag.objects.count()}")
print(f"Total Articles: {Article.objects.count()}")
