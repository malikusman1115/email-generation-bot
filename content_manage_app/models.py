from django.db import models

class HeroSectionContent(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    subheading = models.CharField(max_length=255, default="Proven and Built on Human Decision Science.")
    email_placeholder = models.CharField(max_length=255, default="Enter your email")
    blacklogo = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_bottom_right = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_left = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_section = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_top_right = models.ImageField(upload_to='hero/', blank=True, null=True)
    tick = models.ImageField(upload_to='hero/', blank=True, null=True)

    def __str__(self):
        return self.title or "Hero Section Content"


class StatsSectionContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_image = models.ImageField(upload_to='stats/', blank=True, null=True)
    left_image = models.ImageField(upload_to='stats/', blank=True, null=True)
    right_image = models.ImageField(upload_to='stats/', blank=True, null=True)
    sales_messaging_title = models.CharField(max_length=255, blank=True, null=True)
    sales_messaging_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class BulletPoint(models.Model):
    section = models.ForeignKey(StatsSectionContent, related_name='bullet_points', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Stat(models.Model):
    section = models.ForeignKey(StatsSectionContent, related_name='stats', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.label}: {self.value}"
    

class WorkingSectionContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    button_text = models.CharField(max_length=50, default="Try EngageIQ Free")
    feature_icon = models.ImageField(upload_to='work/', blank=True, null=True)

    def __str__(self):
        return self.title

class Feature(models.Model):
    section = models.ForeignKey(WorkingSectionContent, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class SolutionSectionContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Solution(models.Model):
    section = models.ForeignKey(SolutionSectionContent, related_name='solutions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='solution/', blank=True, null=True)  

    def __str__(self):
        return self.title
    
class LayoutContent(models.Model):
    logo = models.ImageField(upload_to='layout/', blank=True, null=True)
    social_heading = models.CharField(max_length=255, blank=True, null=True)  # ✅ moved here

    def __str__(self):
        return f"LayoutContent #{self.id}"

class NavigationItem(models.Model):
    section = models.ForeignKey(LayoutContent, related_name='navigation_items', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.URLField(default='/')

    def __str__(self):
        return f"{self.label}: {self.url}"

class SocialLink(models.Model):
    section = models.ForeignKey(LayoutContent, related_name='social_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform}: {self.url}"

class CompanyLink(models.Model):
    section = models.ForeignKey(LayoutContent, related_name='company_links', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.URLField()

class ProductLink(models.Model):
    section = models.ForeignKey(LayoutContent, related_name='product_links', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.URLField()
    
class VideoSectionContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Module(models.Model):
    section = models.ForeignKey(VideoSectionContent, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class PaypalSectionContent(models.Model):
    title = models.CharField(max_length=255, default="Complete Your Payment with PayPal")
    heading = models.CharField(max_length=255, default="Choose The Best Pricing Plan for Your Business")  
    description = models.TextField(default="Select a plan and pay securely via PayPal.")
    success_message = models.CharField(max_length=255, default="🎉 Congratulations! Your payment was successful!")

    def __str__(self):
        return self.title
    

class DashboardContent(models.Model):
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)

    border = models.ImageField(upload_to='dashboard/', blank=True, null=True)
    edit = models.ImageField(upload_to='dashboard/', blank=True, null=True)
    header_img = models.ImageField(upload_to='dashboard/', blank=True, null=True)
    home = models.ImageField(upload_to='dashboard/', blank=True, null=True)
    training = models.ImageField(upload_to='dashboard/', blank=True, null=True)
    usage = models.ImageField(upload_to='dashboard/', blank=True, null=True)

    def __str__(self):
        return self.title

class Tooltip(models.Model):
    section = models.ForeignKey(DashboardContent, related_name='tooltips', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class AboutUsContent(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='about_us/', blank=True, null=True)

    def __str__(self):
        return self.heading
    
class ContactUs(models.Model):
    SUBJECT_CHOICES = [
        ('Sales', 'Sales'),
        ('Support', 'Support'),
        ('Feedback', 'Feedback'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
