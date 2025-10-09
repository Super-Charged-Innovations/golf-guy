"""
Internationalization (i18n) Service
Handles Swedish language support and localization
"""
import json
from typing import Dict, Any, Optional
from enum import Enum

class Language(str, Enum):
    """Supported languages"""
    ENGLISH = "en"
    SWEDISH = "sv"

class TranslationService:
    """Service for handling translations and localization"""
    
    def __init__(self):
        self.translations = self._load_translations()
        self.default_language = Language.ENGLISH
        
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translation dictionaries"""
        return {
            Language.ENGLISH: {
                # Navigation
                "nav.destinations": "Destinations",
                "nav.travel_reports": "Travel Reports", 
                "nav.about": "About",
                "nav.contact": "Contact",
                "nav.login": "Sign In",
                "nav.register": "Get Started",
                "nav.logout": "Logout",
                "nav.profile": "My Profile",
                "nav.dashboard": "Dashboard",
                "nav.admin": "Admin",
                
                # Home page
                "home.hero.title": "Discover Your Perfect Golf Destination",
                "home.hero.subtitle": "Personalized golf travel recommendations powered by AI",
                "home.hero.cta": "Start Planning",
                "home.featured.title": "Featured Destinations",
                "home.featured.view_all": "View All Destinations",
                
                # Authentication
                "auth.login.title": "Welcome Back",
                "auth.login.subtitle": "Sign in to access your personalized golf travel dashboard",
                "auth.register.title": "Create Account",
                "auth.register.subtitle": "Join Golf Guy for personalized golf travel recommendations",
                "auth.email": "Email",
                "auth.password": "Password",
                "auth.confirm_password": "Confirm Password",
                "auth.full_name": "Full Name",
                "auth.login_button": "Sign In",
                "auth.register_button": "Create Account",
                "auth.forgot_password": "Forgot your password?",
                "auth.no_account": "Don't have an account? Sign up",
                "auth.have_account": "Already have an account? Sign in",
                
                # Booking system
                "booking.title": "Book Your Golf Experience",
                "booking.check_availability": "Check Availability",
                "booking.select_date": "Select Date",
                "booking.select_time": "Select Time", 
                "booking.players": "Number of Players",
                "booking.special_requests": "Special Requests",
                "booking.total_price": "Total Price",
                "booking.confirm": "Confirm Booking",
                "booking.cancel": "Cancel Booking",
                "booking.status.pending": "Pending Confirmation",
                "booking.status.confirmed": "Confirmed",
                "booking.status.cancelled": "Cancelled",
                
                # Payment system
                "payment.title": "Complete Your Payment",
                "payment.secure": "Secure Payment with Stripe",
                "payment.packages.single_round": "Single Round",
                "payment.packages.premium_round": "Premium Round",
                "payment.packages.golf_lesson": "Golf Lesson",
                "payment.packages.weekend_package": "Weekend Package",
                "payment.packages.luxury_package": "Luxury Experience",
                "payment.processing": "Processing payment...",
                "payment.success": "Payment successful!",
                "payment.failed": "Payment failed",
                "payment.cancelled": "Payment cancelled",
                
                # Search and filters
                "search.title": "Find Your Perfect Golf Destination",
                "search.placeholder": "Search destinations...",
                "search.filters.countries": "Countries",
                "search.filters.price_range": "Price Range",
                "search.filters.dates": "Travel Dates",
                "search.filters.players": "Players",
                "search.filters.accommodation": "Accommodation",
                "search.filters.difficulty": "Course Difficulty",
                "search.filters.type": "Course Type",
                "search.filters.amenities": "Amenities",
                "search.filters.clear": "Clear Filters",
                "search.results.found": "destinations found",
                "search.results.no_results": "No destinations found",
                "search.sort.relevance": "Most Relevant",
                "search.sort.price_asc": "Price: Low to High",
                "search.sort.price_desc": "Price: High to Low",
                
                # Profile and KYC
                "profile.title": "Your Golf Travel Profile",
                "profile.kyc.title": "KYC Documents",
                "profile.tier.explorer": "Explorer",
                "profile.tier.enthusiast": "Enthusiast", 
                "profile.tier.vip": "VIP Golfer",
                
                # GDPR and Privacy
                "gdpr.cookie_consent.title": "Cookie & Privacy Settings",
                "gdpr.cookie_consent.description": "We respect your privacy and are committed to transparency",
                "gdpr.accept_all": "Accept All Cookies",
                "gdpr.reject_all": "Reject All",
                "gdpr.customize": "Customize",
                "gdpr.privacy_policy": "Privacy Policy",
                "gdpr.cookie_policy": "Cookie Policy",
                "gdpr.terms": "Terms of Service",
                
                # Common actions
                "common.save": "Save",
                "common.cancel": "Cancel",
                "common.edit": "Edit",
                "common.delete": "Delete",
                "common.view": "View",
                "common.download": "Download",
                "common.upload": "Upload",
                "common.loading": "Loading...",
                "common.error": "Error",
                "common.success": "Success",
                
                # Currency and formatting
                "currency.sek": "SEK",
                "currency.eur": "EUR",
                "currency.usd": "USD",
                "format.per_person": "per person",
                "format.per_night": "per night"
            },
            
            Language.SWEDISH: {
                # Navigation
                "nav.destinations": "Destinationer",
                "nav.travel_reports": "Reserapporter",
                "nav.about": "Om Oss",
                "nav.contact": "Kontakt",
                "nav.login": "Logga In",
                "nav.register": "Kom Igång",
                "nav.logout": "Logga Ut",
                "nav.profile": "Min Profil",
                "nav.dashboard": "Instrumentpanel",
                "nav.admin": "Admin",
                
                # Home page
                "home.hero.title": "Upptäck Din Perfekta Golfdestination",
                "home.hero.subtitle": "Personliga golfreseförslag drivna av AI",
                "home.hero.cta": "Börja Planera",
                "home.featured.title": "Utvalda Destinationer",
                "home.featured.view_all": "Visa Alla Destinationer",
                
                # Authentication
                "auth.login.title": "Välkommen Tillbaka",
                "auth.login.subtitle": "Logga in för att komma åt din personliga golfreseinstrumentpanel",
                "auth.register.title": "Skapa Konto",
                "auth.register.subtitle": "Gå med i Golf Guy för personliga golfreseförslag",
                "auth.email": "E-post",
                "auth.password": "Lösenord",
                "auth.confirm_password": "Bekräfta Lösenord",
                "auth.full_name": "Fullständigt Namn",
                "auth.login_button": "Logga In",
                "auth.register_button": "Skapa Konto",
                "auth.forgot_password": "Glömt ditt lösenord?",
                "auth.no_account": "Har du inget konto? Registrera dig",
                "auth.have_account": "Har du redan ett konto? Logga in",
                
                # Booking system
                "booking.title": "Boka Din Golfupplevelse",
                "booking.check_availability": "Kontrollera Tillgänglighet",
                "booking.select_date": "Välj Datum",
                "booking.select_time": "Välj Tid",
                "booking.players": "Antal Spelare",
                "booking.special_requests": "Särskilda Önskemål",
                "booking.total_price": "Totalpris",
                "booking.confirm": "Bekräfta Bokning",
                "booking.cancel": "Avboka",
                "booking.status.pending": "Väntar på Bekräftelse",
                "booking.status.confirmed": "Bekräftad",
                "booking.status.cancelled": "Avbokad",
                
                # Payment system
                "payment.title": "Slutför Din Betalning",
                "payment.secure": "Säker Betalning med Stripe",
                "payment.packages.single_round": "Enkel Runda",
                "payment.packages.premium_round": "Premium Runda",
                "payment.packages.golf_lesson": "Golflektion",
                "payment.packages.weekend_package": "Helgpaket",
                "payment.packages.luxury_package": "Lyxupplevelse",
                "payment.processing": "Behandlar betalning...",
                "payment.success": "Betalning lyckades!",
                "payment.failed": "Betalning misslyckades",
                "payment.cancelled": "Betalning avbruten",
                
                # Search and filters
                "search.title": "Hitta Din Perfekta Golfdestination",
                "search.placeholder": "Sök destinationer...",
                "search.filters.countries": "Länder",
                "search.filters.price_range": "Prisintervall",
                "search.filters.dates": "Resedatum",
                "search.filters.players": "Spelare",
                "search.filters.accommodation": "Boende",
                "search.filters.difficulty": "Bansvårighet",
                "search.filters.type": "Bantyp",
                "search.filters.amenities": "Bekvämligheter",
                "search.filters.clear": "Rensa Filter",
                "search.results.found": "destinationer hittades",
                "search.results.no_results": "Inga destinationer hittades",
                "search.sort.relevance": "Mest Relevanta",
                "search.sort.price_asc": "Pris: Låg till Hög",
                "search.sort.price_desc": "Pris: Hög till Låg",
                
                # Profile and KYC
                "profile.title": "Din Golfreseprofil",
                "profile.kyc.title": "KYC Dokument",
                "profile.tier.explorer": "Upptäckare",
                "profile.tier.enthusiast": "Entusiast",
                "profile.tier.vip": "VIP Golfspelare",
                
                # GDPR and Privacy
                "gdpr.cookie_consent.title": "Cookie- och Integritetsinställningar",
                "gdpr.cookie_consent.description": "Vi respekterar din integritet och är engagerade i transparens",
                "gdpr.accept_all": "Acceptera Alla Cookies",
                "gdpr.reject_all": "Avvisa Alla",
                "gdpr.customize": "Anpassa",
                "gdpr.privacy_policy": "Integritetspolicy",
                "gdpr.cookie_policy": "Cookie-policy",
                "gdpr.terms": "Användarvillkor",
                
                # Common actions
                "common.save": "Spara",
                "common.cancel": "Avbryt",
                "common.edit": "Redigera",
                "common.delete": "Ta Bort",
                "common.view": "Visa",
                "common.download": "Ladda Ner",
                "common.upload": "Ladda Upp",
                "common.loading": "Laddar...",
                "common.error": "Fel",
                "common.success": "Framgång",
                
                # Currency and formatting
                "currency.sek": "SEK",
                "currency.eur": "EUR", 
                "currency.usd": "USD",
                "format.per_person": "per person",
                "format.per_night": "per natt"
            }
        }
    
    def get_translation(self, key: str, language: Language = Language.ENGLISH) -> str:
        """Get translation for a specific key"""
        
        translations = self.translations.get(language, {})
        return translations.get(key, key)  # Return key if translation not found
    
    def get_all_translations(self, language: Language = Language.ENGLISH) -> Dict[str, str]:
        """Get all translations for a language"""
        return self.translations.get(language, {})
    
    def format_currency(self, amount: float, currency: str = "SEK", language: Language = Language.ENGLISH) -> str:
        """Format currency according to language preferences"""
        
        if language == Language.SWEDISH:
            if currency == "SEK":
                return f"{amount:,.0f} kr"
            elif currency == "EUR":
                return f"€{amount:,.0f}"
            else:
                return f"{amount:,.0f} {currency}"
        else:  # English
            if currency == "SEK":
                return f"{amount:,.0f} SEK"
            elif currency == "EUR":
                return f"€{amount:,.0f}"
            elif currency == "USD":
                return f"${amount:,.0f}"
            else:
                return f"{amount:,.0f} {currency}"
    
    def format_date(self, date_obj, language: Language = Language.ENGLISH) -> str:
        """Format date according to language preferences"""
        
        if language == Language.SWEDISH:
            # Swedish date format: "15 oktober 2024"
            months_sv = [
                "januari", "februari", "mars", "april", "maj", "juni",
                "juli", "augusti", "september", "oktober", "november", "december"
            ]
            return f"{date_obj.day} {months_sv[date_obj.month-1]} {date_obj.year}"
        else:
            # English date format: "October 15, 2024"
            return date_obj.strftime("%B %d, %Y")
    
    def get_country_name(self, country_code: str, language: Language = Language.ENGLISH) -> str:
        """Get localized country names"""
        
        country_names = {
            Language.ENGLISH: {
                "spain": "Spain",
                "portugal": "Portugal", 
                "scotland": "Scotland",
                "ireland": "Ireland",
                "england": "England",
                "france": "France",
                "italy": "Italy",
                "turkey": "Turkey",
                "morocco": "Morocco",
                "dubai": "Dubai",
                "thailand": "Thailand",
                "mauritius": "Mauritius",
                "south_africa": "South Africa",
                "sweden": "Sweden"
            },
            Language.SWEDISH: {
                "spain": "Spanien",
                "portugal": "Portugal",
                "scotland": "Skottland", 
                "ireland": "Irland",
                "england": "England",
                "france": "Frankrike",
                "italy": "Italien",
                "turkey": "Turkiet",
                "morocco": "Marocko",
                "dubai": "Dubai",
                "thailand": "Thailand",
                "mauritius": "Mauritius",
                "south_africa": "Sydafrika",
                "sweden": "Sverige"
            }
        }
        
        country_key = country_code.lower().replace(" ", "_")
        return country_names.get(language, {}).get(country_key, country_code)

# Global translation service
translation_service = TranslationService()

# Utility functions for templates
def t(key: str, language: str = "en") -> str:
    """Quick translation function"""
    lang = Language.SWEDISH if language == "sv" else Language.ENGLISH
    return translation_service.get_translation(key, lang)

def format_price(amount: float, currency: str = "SEK", language: str = "en") -> str:
    """Quick price formatting function"""
    lang = Language.SWEDISH if language == "sv" else Language.ENGLISH
    return translation_service.format_currency(amount, currency, lang)