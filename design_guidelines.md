{
  "meta": {
    "product": "Premium Golf Travel Booking Platform",
    "audience": "Swedish golf travelers booking custom golf vacations (mobile-first)",
    "brand_attributes": ["professional", "trustworthy", "premium", "content-led", "service-oriented"],
    "success_actions": [
      "Search destinations/courses",
      "View package details & galleries",
      "Add rounds/rooms/dates",
      "Send booking inquiry / start checkout",
      "Call/Chat with specialist",
      "Read testimonials & trust badges"
    ]
  },

  "inspiration_sources": [
    {
      "name": "Golfbreaks",
      "url": "https://www.golfbreaks.com/en-us/",
      "notes": "Aspirational hero, rewards/trust, strong CTAs near fold"
    },
    {
      "name": "Your Golf Travel",
      "url": "https://www.yourgolftravel.com",
      "notes": "Destination cards, trust logos (ATOL/insurance), robust filters"
    },
    {
      "name": "NNG carousels guidance",
      "url": "https://www.nngroup.com/articles/designing-effective-carousels/",
      "notes": "Mobile carousel best practices (controls, swipe, pause)"
    },
    {
      "name": "Justinmind carousel patterns",
      "url": "https://www.justinmind.com/ui-design/carousel",
      "notes": "Show next-slide preview, clear controls"
    }
  ],

  "design_personality": {
    "tone": "Premium Nordic leisure with editorial clarity",
    "style_fusion": [
      "Swiss Style grid discipline for content readability",
      "Luxury accents (subtle gold) for highlights and CTAs",
      "Glassmorphism for secondary surfaces on imagery (max 20% area)",
      "Bento grid for featured destinations"
    ]
  },

  "design_tokens": {
    "colors": {
      "description": "HSL tokens to override in /app/frontend/src/index.css :root and .dark",
      "light": {
        "--background": "60 11% 98%",          
        "--foreground": "223 15% 12%",          
        "--card": "0 0% 100%",
        "--card-foreground": "223 15% 12%",
        "--popover": "0 0% 100%",
        "--popover-foreground": "223 15% 12%",
        "--primary": "151 45% 30%",             
        "--primary-foreground": "0 0% 98%",
        "--secondary": "210 28% 97%",           
        "--secondary-foreground": "223 15% 12%",
        "--accent": "45 42% 56%",               
        "--accent-foreground": "223 15% 12%",
        "--muted": "210 18% 95%",
        "--muted-foreground": "223 11% 36%",
        "--border": "210 16% 88%",
        "--input": "210 16% 88%",
        "--ring": "210 100% 40%",              
        "--success": "151 45% 30%",
        "--info": "210 80% 36%",
        "--warning": "45 90% 55%",
        "--destructive": "3 84% 60%",
        "--destructive-foreground": "0 0% 98%",
        "--gold-soft": "45 30% 60%",
        "--navy-soft": "210 25% 20%",
        "--sand": "48 31% 90%",
        "--sky-mist": "210 40% 97%"
      },
      "dark": {
        "--background": "223 16% 8%",
        "--foreground": "0 0% 98%",
        "--card": "223 16% 10%",
        "--card-foreground": "0 0% 98%",
        "--popover": "223 16% 10%",
        "--popover-foreground": "0 0% 98%",
        "--primary": "151 35% 55%",             
        "--primary-foreground": "223 16% 8%",
        "--secondary": "223 16% 14%",
        "--secondary-foreground": "0 0% 98%",
        "--accent": "45 42% 56%",
        "--accent-foreground": "223 16% 8%",
        "--muted": "223 16% 14%",
        "--muted-foreground": "0 0% 70%",
        "--border": "223 16% 20%",
        "--input": "223 16% 20%",
        "--ring": "151 45% 45%",
        "--success": "151 45% 45%",
        "--info": "210 80% 60%",
        "--warning": "45 90% 65%",
        "--destructive": "3 62% 45%",
        "--destructive-foreground": "0 0% 98%",
        "--gold-soft": "45 30% 60%",
        "--navy-soft": "223 25% 20%",
        "--sand": "48 15% 25%",
        "--sky-mist": "210 12% 20%"
      },
      "charts": {
        "--chart-1": "151 45% 38%",
        "--chart-2": "210 66% 40%",
        "--chart-3": "45 70% 50%",
        "--chart-4": "223 20% 45%",
        "--chart-5": "3 70% 58%"
      }
    },
    "gradients": {
      "rules": [
        "Never exceed 20% of viewport area",
        "Use on section backgrounds and hero only; not inside content blocks",
        "Avoid dark/saturated combos and purple/pink stacks",
        "No gradients on small UI (<100px)"
      ],
      "safe_gradients": [
        {"name": "Dawn Fairway", "css": "linear-gradient(135deg, hsl(151 45% 96%) 0%, hsl(210 40% 97%) 50%, hsl(48 31% 96%) 100%)"},
        {"name": "Sea to Green", "css": "linear-gradient(120deg, hsl(210 66% 96%) 0%, hsl(151 45% 94%) 100%)"},
        {"name": "Sand Edge", "css": "linear-gradient(180deg, hsl(48 31% 95%) 0%, hsl(0 0% 100%) 100%)"}
      ]
    },
    "typography": {
      "web_fonts": [
        {
          "family": "Playfair Display",
          "weights": [400, 500, 700],
          "usage": "Headings (luxury feel)"
        },
        {
          "family": "Karla",
          "weights": [400, 500, 600, 700],
          "usage": "Body, UI controls, forms (high legibility)"
        },
        {
          "family": "Chivo",
          "weights": [400, 600, 700],
          "usage": "Admin dashboard UI and charts labels"
        }
      ],
      "tailwind_classes": {
        "h1": "font-playfair text-4xl sm:text-5xl lg:text-6xl tracking-tight",
        "h2": "font-playfair text-base md:text-lg",
        "body": "font-karla text-base md:text-base text-foreground/90",
        "small": "text-sm text-foreground/70",
        "eyebrow": "uppercase tracking-[0.2em] text-xs text-foreground/60"
      }
    },
    "spacing": {
      "scale": [0,4,8,12,16,24,32,40,48,64,80,96],
      "container": {
        "mobile": "px-4",
        "tablet": "px-6",
        "desktop": "px-8 max-w-[1200px] mx-auto"
      }
    },
    "radii": {
      "--radius": "0.75rem",
      "button": "0.75rem",
      "card": "1rem",
      "image": "0.75rem"
    },
    "shadows": {
      "elevation-1": "0 1px 2px rgba(0,0,0,0.06)",
      "elevation-2": "0 4px 12px rgba(0,0,0,0.08)",
      "elevation-3": "0 12px 24px rgba(0,0,0,0.12)"
    },
    "z_index": {"nav": 50, "overlay": 40, "modal": 60},
    "breakpoints": {"sm": 640, "md": 768, "lg": 1024, "xl": 1280}
  },

  "color_usage_rules": {
    "primary": "Use fairway green for primary actions and highlights",
    "accent": "Gold for premium hints: prices, ratings stars, small borders",
    "neutral_backgrounds": "White or very light sand for content blocks and cards",
    "dark_sections": "Optional dark navy sections for contrast (no gradients)",
    "links": "Blue/teal info color for secondary links",
    "borders": "Use cool gray (border token) at 1px or 1.5px",
    "error_warning_success": {
      "error": "--destructive",
      "warning": "--warning",
      "success": "--success"
    },
    "hero_example": "Use 'Dawn Fairway' gradient on hero background only, overlay with 8-12% black scrim over imagery to preserve text contrast"
  },

  "layout_system": {
    "page_templates": {
      "home": [
        "Top bar with compact search (dates, golfers, rooms)",
        "Hero split-screen: copy left, swipe carousel right (shows next-slide bleed)",
        "Bento featured grid: 2x2 cards (Spain, Portugal, Turkey, Sweden)",
        "Trust bar: insurance + partners + rating badges",
        "Editorial strip: latest travel reports",
        "CTA band: 'Get custom quote' with phone + form"
      ],
      "destination_listing": [
        "Filter rail (Sheet on mobile) with Select, Slider, Calendar",
        "Card grid 2-col mobile, 3-col desktop",
        "Sticky bottom CTA on mobile: 'Start enquiry'"
      ],
      "package_detail": [
        "Gallery (carousel + thumbnails)",
        "Key facts (par, holes, difficulty, season) + map",
        "Itinerary tabs (tabs component)",
        "Sticky enquiry drawer with price summary"
      ],
      "content_article": [
        "Magazine layout with large lead image",
        "Sidebar on desktop for related trips",
        "Readable 70ch measure, generous line-height"
      ]
    },
    "grids": {
      "content_width": "max-w-[1200px] mx-auto",
      "columns": "12-col grid desktop, 4-col mobile",
      "gaps": "gap-4 sm:gap-6 lg:gap-8"
    }
  },

  "buttons": {
    "style": "Luxury / Elegant",
    "tokens": {
      "--btn-radius": "0.75rem",
      "--btn-shadow": "0 6px 18px rgba(0,0,0,0.10)",
      "--btn-motion": "transition-colors transition-shadow duration-200 ease-out"
    },
    "variants": {
      "primary": "bg-[hsl(151_45%_30%)] text-white hover:bg-[hsl(151_45%_26%)] focus-visible:ring-2 focus-visible:ring-[hsl(210_66%_40%)]",
      "secondary": "bg-white text-[hsl(151_45%_30%)] border border-[hsl(210_16%_88%)] hover:border-[hsl(151_45%_30%)]",
      "ghost": "bg-transparent text-foreground hover:bg-[hsl(210_28%_97%)]"
    },
    "sizes": {
      "sm": "px-4 py-2 text-sm",
      "md": "px-5 py-2.5 text-base",
      "lg": "px-6 py-3 text-base"
    }
  },

  "component_path": {
    "Accordion": "./components/ui/accordion",
    "Alert": "./components/ui/alert",
    "AlertDialog": "./components/ui/alert-dialog",
    "AspectRatio": "./components/ui/aspect-ratio",
    "Avatar": "./components/ui/avatar",
    "Badge": "./components/ui/badge",
    "Breadcrumb": "./components/ui/breadcrumb",
    "Button": "./components/ui/button",
    "Calendar": "./components/ui/calendar",
    "Card": "./components/ui/card",
    "Carousel": "./components/ui/carousel",
    "Checkbox": "./components/ui/checkbox",
    "Collapsible": "./components/ui/collapsible",
    "Command": "./components/ui/command",
    "Dialog": "./components/ui/dialog",
    "Drawer": "./components/ui/drawer",
    "DropdownMenu": "./components/ui/dropdown-menu",
    "Form": "./components/ui/form",
    "HoverCard": "./components/ui/hover-card",
    "Input": "./components/ui/input",
    "Label": "./components/ui/label",
    "Menubar": "./components/ui/menubar",
    "NavigationMenu": "./components/ui/navigation-menu",
    "Pagination": "./components/ui/pagination",
    "Popover": "./components/ui/popover",
    "Progress": "./components/ui/progress",
    "RadioGroup": "./components/ui/radio-group",
    "Resizable": "./components/ui/resizable",
    "ScrollArea": "./components/ui/scroll-area",
    "Select": "./components/ui/select",
    "Separator": "./components/ui/separator",
    "Sheet": "./components/ui/sheet",
    "Skeleton": "./components/ui/skeleton",
    "Slider": "./components/ui/slider",
    "Sonner": "./components/ui/sonner",
    "Switch": "./components/ui/switch",
    "Table": "./components/ui/table",
    "Tabs": "./components/ui/tabs",
    "Textarea": "./components/ui/textarea",
    "Toast": "./components/ui/toast",
    "Toaster": "./components/ui/toaster",
    "Toggle": "./components/ui/toggle",
    "ToggleGroup": "./components/ui/toggle-group",
    "Tooltip": "./components/ui/tooltip"
  },

  "component_guidelines": [
    {
      "name": "HeroCarousel",
      "purpose": "Aspirational image-led entry point with clear booking CTA",
      "composition": ["Carousel", "Button", "Badge"],
      "rules": [
        "Show next-slide bleed on mobile (peek of 12px)",
        "Manual swipe enabled; auto-rotate max 6s with pause on hover/focus",
        "Text overlay gradient: 8-12% black to ensure AA contrast",
        "Primary CTA visible in first slide",
        "Add data-testid attributes to controls and CTA"
      ],
      "testid_examples": [
        "data-testid=\"hero-carousel\"",
        "data-testid=\"hero-next-button\"",
        "data-testid=\"hero-cta-button\""
      ]
    },
    {
      "name": "DestinationCard",
      "purpose": "Display course/resort with price from, rating, quick facts",
      "composition": ["Card", "Badge", "Button", "Avatar (flag)", "Tooltip"],
      "states": ["default", "hover-elevated", "loading-skeleton"],
      "rules": [
        "Image aspect 4:3 (AspectRatio)",
        "Hover: subtle lift and shadow-elevation-2",
        "Include quick tags (par, holes) as badges",
        "Ratings use gold accent stars",
        "Add data-testid on root and CTA"
      ],
      "testid_examples": [
        "data-testid=\"destination-card\"",
        "data-testid=\"destination-card-cta-button\""
      ]
    },
    {
      "name": "SearchFilters",
      "purpose": "Find trips by date, nights, golfers, budget, region",
      "composition": ["Sheet (mobile)", "Select", "Slider", "Calendar", "Checkbox", "Button"],
      "rules": [
        "Mobile: open as bottom sheet with big tap targets",
        "Desktop: left rail collapsible",
        "Calendar: shadcn calendar only",
        "Budget: Slider with step 500 SEK",
        "Include 'Clear all' ghost button"
      ],
      "testid_examples": [
        "data-testid=\"filters-open-button\"",
        "data-testid=\"filters-apply-button\"",
        "data-testid=\"filters-clear-button\""
      ]
    },
    {
      "name": "TrustBar",
      "purpose": "Show insurance partners, memberships, review scores",
      "composition": ["ScrollArea", "Tooltip"],
      "rules": [
        "Grayscale logos with 60% opacity, hover to 100%",
        "ARIA labels on each logo",
        "Include rating badge with gold accent"
      ],
      "testid_examples": ["data-testid=\"trustbar\""]
    },
    {
      "name": "StickyEnquiryDrawer",
      "purpose": "Sticky mobile CTA opening a Drawer with enquiry form",
      "composition": ["Drawer", "Form", "Input", "Select", "Calendar", "Textarea", "Sonner"],
      "rules": [
        "Button spans full width on mobile",
        "Show price summary and inclusions",
        "On submit: Sonner toast and focus management"
      ],
      "testid_examples": [
        "data-testid=\"enquiry-open-button\"",
        "data-testid=\"enquiry-submit-button\""
      ]
    },
    {
      "name": "TestimonialCard",
      "purpose": "Professional testimonial with avatar, rating, trip meta",
      "composition": ["Card", "Avatar", "Badge", "Separator"],
      "rules": [
        "Use editorial quote style with Playfair for the quote",
        "Stars in gold, text in high contrast",
        "Max width 60ch for readability"
      ],
      "testid_examples": ["data-testid=\"testimonial-card\""]
    },
    {
      "name": "GalleryCarousel",
      "purpose": "Course/resort media gallery with thumbnails",
      "composition": ["Carousel", "AspectRatio", "Dialog (lightbox)"],
      "rules": [
        "Lazy-load off-screen images",
        "Keyboard nav in dialog",
        "Captions in small text below"
      ],
      "testid_examples": ["data-testid=\"gallery-carousel\""]
    }
  ],

  "motion_and_microinteractions": {
    "principles": [
      "Purposeful, short, never block user",
      "Hover elevation and border emphasis on actionable cards",
      "Entrance: fade-up 20px at 250–350ms stagger",
      "Buttons: subtle scale 0.98 on press"
    ],
    "libraries": ["framer-motion"],
    "tailwind_helpers": ["motion-reduce:transition-none", "will-change-transform"],
    "examples": {
      "card_hover": "hover:shadow-[var(--shadow-elevation-2)] hover:-translate-y-0.5 transition-shadow transition-transform duration-200 ease-out",
      "button": "transition-colors duration-200 ease-out focus-visible:outline-none focus-visible:ring-2"
    }
  },

  "accessibility": {
    "contrast": "Maintain WCAG AA (min 4.5:1) for text on imagery with scrims",
    "focus": "Always visible focus states (ring tokens)",
    "motion_reduction": "Respect prefers-reduced-motion: reduce or disable animations",
    "tap_targets": ">= 44px on mobile",
    "language": "Provide sv-SE labels and SEK currency formatting",
    "icons": "Use lucide-react or FontAwesome; no emoji icons"
  },

  "image_urls": [
    {
      "category": "hero",
      "description": "Sunrise over a premium golf course, reflective water",
      "url": "https://images.unsplash.com/photo-1683836018144-6e5f398102de?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBnb2xmJTIwY291cnNlJTIwc3VucmlzZSUyMGFlcmlhbCUyMGZhaXJ3YXl8ZW58MHx8fHwxNzU5OTM4ODQ3fDA&ixlib=rb-4.1.0&q=85"
    },
    {
      "category": "destinations",
      "description": "Hot air balloon over lake by a green – aspirational travel",
      "url": "https://images.unsplash.com/photo-1602798416092-03afbccf616a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBnb2xmJTIwY291cnNlJTIwc3VucmlzZSUyMGFlcmlhbCUyMGZhaXJ3YXl8ZW58MHx8fHwxNzU5OTM4ODQ3fDA&ixlib=rb-4.1.0&q=85"
    },
    {
      "category": "gallery",
      "description": "Aerial course with water and trees – texture-rich overhead",
      "url": "https://images.unsplash.com/photo-1668890966028-889d8f67f2b1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBnb2xmJTIwY291cnNlJTIwc3VucmlzZSUyMGFlcmlhbCUyMGZhaXJ3YXl8ZW58MHx8fHwxNzU5OTM4ODQ3fDA&ixlib=rb-4.1.0&q=85"
    },
    {
      "category": "gallery",
      "description": "Top-down bunker and green composition",
      "url": "https://images.unsplash.com/photo-1605144884288-49eb7f9bb447?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBnb2xmJTIwY291cnNlJTIwc3VucmlzZSUyMGFlcmlhbCUyMGZhaXJ3YXl8ZW58MHx8fHwxNzU5OTM4ODQ3fDA&ixlib=rb-4.1.0&q=85"
    },
    {
      "category": "testimonial",
      "description": "Golfer at sunset – human story angle",
      "url": "https://images.pexels.com/photos/6256828/pexels-photo-6256828.jpeg"
    }
  ],

  "libraries": {
    "primary": [
      "shadcn/ui (already included in ./components/ui)",
      "Tailwind CSS",
      "Sonner for toasts (./components/ui/sonner)"
    ],
    "additional": [
      {
        "name": "framer-motion",
        "install": "npm i framer-motion",
        "use": "Entrance and hover micro-interactions for cards and sections"
      },
      {
        "name": "recharts",
        "install": "npm i recharts",
        "use": "Admin dashboard KPIs, bookings over time, top destinations"
      }
    ]
  },

  "code_scaffolds": {
    "note": "All code in .jsx/.js (no .tsx). Always add data-testid attributes.",
    "hero_carousel.jsx": "import { Carousel } from './components/ui/carousel';\nimport { Button } from './components/ui/button';\n\nexport const HeroCarousel = ({ slides }) => {\n  return (\n    <section className=\"relative\" data-testid=\"hero-carousel\">\n      <Carousel options={{ loop: true }} className=\"w-full\">\n        {slides.map((s, idx) => (\n          <div key={idx} className=\"relative\">\n            <div className=\"absolute inset-0 bg-black/20\" aria-hidden=\"true\" />\n            <img src={s.image} alt={s.alt} className=\"h-[56vh] w-full object-cover sm:rounded-xl\" />\n            <div className=\"absolute inset-x-4 bottom-6 sm:inset-x-8 sm:bottom-10 text-white max-w-xl\">\n              <p className=\"uppercase tracking-[0.2em] text-xs\">{s.kicker}</p>\n              <h1 className=\"font-playfair text-4xl sm:text-5xl lg:text-6xl\">{s.title}</h1>\n              <p className=\"mt-2 max-w-prose\">{s.subtitle}</p>\n              <div className=\"mt-4 flex gap-3\">\n                <Button data-testid=\"hero-cta-button\" className=\"bg-[hsl(151_45%_30%)] text-white hover:bg-[hsl(151_45%_26%)]\">Starta förfrågan</Button>\n                <Button variant=\"secondary\" className=\"bg-white text-[hsl(151_45%_30%)]\">Se erbjudanden</Button>\n              </div>\n            </div>\n          </div>\n        ))}\n      </Carousel>\n    </section>\n  );\n};\n",
    "destination_card.jsx": "import { Card } from './components/ui/card';\nimport { Button } from './components/ui/button';\nimport { Badge } from './components/ui/badge';\nimport { AspectRatio } from './components/ui/aspect-ratio';\n\nexport const DestinationCard = ({ item }) => {\n  return (\n    <Card data-testid=\"destination-card\" className=\"group overflow-hidden border bg-white hover:shadow-lg transition-shadow duration-200\">\n      <div className=\"relative\">\n        <AspectRatio ratio={4/3}>\n          <img src={item.image} alt={item.title} className=\"h-full w-full object-cover\" />\n        </AspectRatio>\n        <div className=\"absolute top-3 left-3 flex gap-2\">\n          {item.tags?.map((t) => <Badge key={t} className=\"bg-white/90 text-foreground\">{t}</Badge>)}\n        </div>\n      </div>\n      <div className=\"p-4\">\n        <h3 className=\"font-playfair text-lg\">{item.title}</h3>\n        <p className=\"text-sm text-foreground/70 mt-1\">{item.location}</p>\n        <div className=\"mt-3 flex items-center justify-between\">\n          <span className=\"text-sm\">från <span className=\"font-semibold\">{item.priceSek} SEK</span></span>\n          <Button data-testid=\"destination-card-cta-button\" size=\"sm\">Visa paket</Button>\n        </div>\n      </div>\n    </Card>\n  );\n};\n",
    "sticky_enquiry_drawer.jsx": "import { Drawer } from './components/ui/drawer';\nimport { Button } from './components/ui/button';\nimport { Input } from './components/ui/input';\nimport { Select } from './components/ui/select';\nimport { Calendar } from './components/ui/calendar';\nimport { Textarea } from './components/ui/textarea';\nimport { Toaster } from './components/ui/toaster';\nimport { toast } from './components/ui/sonner';\nimport { useState } from 'react';\n\nexport const StickyEnquiryDrawer = () => {\n  const [open, setOpen] = useState(false);\n  return (\n    <>\n      <div className=\"fixed inset-x-0 bottom-0 z-50 bg-white/90 backdrop-blur border-t p-3 sm:hidden\">\n        <Button data-testid=\"enquiry-open-button\" onClick={() => setOpen(true)} className=\"w-full\">Starta förfrågan</Button>\n      </div>\n      <Drawer open={open} onOpenChange={setOpen}>\n        <div className=\"p-4 space-y-3\">\n          <h3 className=\"font-playfair text-xl\">Dina önskemål</h3>\n          <Input placeholder=\"Namn\" data-testid=\"enquiry-name-input\" />\n          <Input placeholder=\"E-post\" type=\"email\" data-testid=\"enquiry-email-input\" />\n          <div className=\"grid grid-cols-2 gap-2\">\n            <Input placeholder=\"Golfare\" type=\"number\" />\n            <Input placeholder=\"Nätter\" type=\"number\" />\n          </div>\n          <div className=\"border rounded-md p-2\"><Calendar mode=\"single\" /></div>\n          <Textarea placeholder=\"Berätta mer...\" />\n          <Button data-testid=\"enquiry-submit-button\" onClick={() => { toast.success('Förfrågan skickad'); setOpen(false); }}>Skicka</Button>\n        </div>\n      </Drawer>\n      <Toaster />\n    </>\n  );\n};\n",
    "filters_sheet.jsx": "import { Sheet } from './components/ui/sheet';\nimport { Button } from './components/ui/button';\nimport { Select } from './components/ui/select';\nimport { Slider } from './components/ui/slider';\nimport { Calendar } from './components/ui/calendar';\nimport { useState } from 'react';\n\nexport const FiltersSheet = () => {\n  const [open, setOpen] = useState(false);\n  return (\n    <>\n      <Button data-testid=\"filters-open-button\" variant=\"secondary\" onClick={() => setOpen(true)}>Filter</Button>\n      <Sheet open={open} onOpenChange={setOpen}>\n        <div className=\"p-4 space-y-4\">\n          <Select>/* region */</Select>\n          <div>\n            <label className=\"text-sm\">Budget (SEK)</label>\n            <Slider min={0} max={50000} step={500} defaultValue={[10000]} />\n          </div>\n          <div className=\"border rounded-md p-2\"><Calendar mode=\"range\" /></div>\n          <div className=\"flex gap-2\">\n            <Button data-testid=\"filters-apply-button\">Apply</Button>\n            <Button data-testid=\"filters-clear-button\" variant=\"ghost\">Clear all</Button>\n          </div>\n        </div>\n      </Sheet>\n    </>\n  );\n};\n"
  },

  "admin_dashboard_guidelines": {
    "colors": "Prefer neutral background with green/blue accents for charts; avoid gradients in data surfaces",
    "typography": "Chivo for headings, Karla for table content",
    "components": ["Tabs for sections", "Table for bookings", "Select for filters", "Recharts line/bar/pie"],
    "empty_states": "Use muted illustrations or simple icons with 'No data yet' and primary CTA",
    "charts": {
      "line": "Bookings per week",
      "bar": "Top destinations",
      "pie": "Channel split"
    }
  },

  "data_testid_policy": {
    "convention": "kebab-case describing role, e.g., booking-cta-button, destination-card",
    "scope": "All interactive and key informational elements (buttons, links, inputs, menus, errors, totals)",
    "examples": [
      "data-testid=\"booking-cta-button\"",
      "data-testid=\"price-summary-text\"",
      "data-testid=\"login-form-submit-button\""
    ]
  },

  "instructions_to_main_agent": [
    "Fonts: Load Google Fonts for 'Playfair Display', 'Karla', and 'Chivo' in index.html and map Tailwind utilities via font-family in globals (e.g., .font-playfair, .font-karla)",
    "Update /app/frontend/src/index.css :root and .dark color tokens with the 'design_tokens.colors' values",
    "Apply gradient only on hero sections using 'design_tokens.gradients.safe_gradients' and enforce the gradient restriction rule",
    "Use shadcn components from component_path; no native HTML fallbacks for dropdowns, dialogs, or calendars",
    "Ensure all interactive elements have data-testid attributes following the provided policy",
    "Mobile-first: implement sticky bottom enquiry button and sheet filters; desktop can show rail filters",
    "Use Sonner in ./components/ui/sonner for toasts; include <Toaster /> once",
    "Remember: never use universal transition: all; scope transitions to color, shadow, or opacity only",
    "Spacing: prefer larger paddings (2–3x baseline) and 70ch max-width for long-form content",
    "Icons: Use lucide-react or FontAwesome CDN (no emoji icons)"
  ],

  "general_ui_ux_guidelines_raw": "- You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n- You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n- NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals."
}
