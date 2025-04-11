from h2o_wave import main, app, Q, ui
import pycountry

"""
    xs: 0px for extra small devices (portrait phones)
    s: 576px for small devices (landscape phones)
    m: 768px for medium devices (tablets)
    l: 992px for large devices (desktops)
    xl: 1200px for extra large devices (large desktops).
"""

choices = [ui.choice(name=country.name, label=country.name) for country in pycountry.countries]
restrictions = ['Vegetarian', 'Vegan', 'Gluten Free', 'Halal', 'Kosher']
travel_styles = [
    "Nature", "Adventure", "Beach", "Culture & History", "Luxury",
    "Budget", "Food & Drink", "Nightlife", "Wellness & Spa", "Shopping"
]

@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        q.client.themeArg = True
        q.client.themeName = 'default'
        q.client.themeNameText = 'Dark'
        q.client.initialized = True
        q.client.restrictions = []

    if q.args.theme:
        q.client.themeArg = not q.client.themeArg

    if q.client.themeArg:
        q.client.themeName = 'default'
        q.client.themeNameText = 'Dark'
    else:
        q.client.themeName = 'h2o-dark'
        q.client.themeNameText = 'Light'

    # Layout
    q.page['meta'] = ui.meta_card(
        box='',
        theme=q.client.themeName,
        layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone(name='header'),
                    ui.zone(
                        name='content',
                        direction=ui.ZoneDirection.COLUMN,
                        size='100%',
                        zones=[
                            ui.zone(
                                name='content-left',
                                direction=ui.ZoneDirection.COLUMN,
                                size='50%',
                                zones=[ui.zone(name='content-left-column', direction=ui.ZoneDirection.COLUMN)]
                            ),
                            ui.zone(
                                name='content-right',
                                direction=ui.ZoneDirection.COLUMN,
                                size='50%',
                                zones=[ui.zone(name='content-right-column', direction=ui.ZoneDirection.COLUMN)]
                            ),
                        ]
                    ),
                    ui.zone(name='footer'),
                ]
            ),
            ui.layout(
                breakpoint='l',
                zones=[
                    ui.zone(name='header'),
                    ui.zone(
                        name='content',
                        direction=ui.ZoneDirection.ROW,
                        size='100%',
                        zones=[
                            ui.zone(
                                name='content-left',
                                direction=ui.ZoneDirection.COLUMN,
                                size='50%',
                                zones=[ui.zone(name='content-left-column', direction=ui.ZoneDirection.COLUMN)]
                            ),
                            ui.zone(
                                name='content-right',
                                direction=ui.ZoneDirection.COLUMN,
                                size='50%',
                                zones=[ui.zone(name='content-right-column', direction=ui.ZoneDirection.COLUMN)]
                            ),
                        ]
                    ),
                    ui.zone(name='footer'),
                ]
            )
        ]
    )

    # Header
    q.page['header'] = ui.header_card(
        box='header',
        title='Wayo | AI for everything',
        subtitle='LLM powered by H2O Wave',
        image='https://wave.h2o.ai/img/h2o-logo.svg',
        items=[ui.button(name='theme', label=q.client.themeNameText)]
    )


    # Country & Travelers Form
    q.page['left-form'] = ui.form_card(
        box='content-left-column',
        title='',
        items=[
            ui.text('### ✈️ **Travel Preferences**'),
            ui.dropdown(name='selected_countries', label='Country', value='B', required=True, choices=choices),
            ui.spinbox(name='member_count', label='How many people are traveling?', min=1, max=10, value=2),
            ui.spinbox(name='trip_days', label='How many days is your trip?', min=1, max=30, value=2),
        ]
    )

    # Travel Style Checklist
    q.page['left-form-3'] = ui.form_card(
        box='content-left-column',
        title='',
        items=[
            ui.checklist(
                name='travel_styles',
                label='What kind of experiences are you looking for?',
                inline=True,
                choices=[
                    ui.choice(name='Nature', label='Nature'),
                    ui.choice(name='Adventure', label='Adventure'),
                    ui.choice(name='Beach', label='Beach'),
                    ui.choice(name='Culture & History', label='Culture & History'),
                    ui.choice(name='Luxury', label='Luxury'),
                    ui.choice(name='Budget', label='Budget'),
                    ui.choice(name='Food & Drink', label='Food & Drink'),
                    ui.choice(name='Nightlife', label='Nightlife'),
                    ui.choice(name='Wellness & Spa', label='Wellness & Spa'),
                    ui.choice(name='Shopping', label='Shopping'),
                ]
            )
        ]
    )

    # Meal Preferences Checklist
    q.page['left-form-4'] = ui.form_card(
        box="content-left-column",
        title='',
        items=[
            ui.checklist(
                name='meal_preferences',
                label='Do you have any meal preferences?',
                inline=True,
                values=[],
                choices=[
                    ui.choice(name='Vegetarian', label='Vegetarian'),
                    ui.choice(name='Vegan', label='Vegan'),
                    ui.choice(name='Gluten-Free', label='Gluten-Free'),
                    ui.choice(name='Halal', label='Halal'),
                    ui.choice(name='Kosher', label='Kosher'),
                    ui.choice(name='Seafood', label='Seafood'),
                    ui.choice(name='Local Cuisine', label='Local Cuisine'),
                    ui.choice(name='No Preference', label='No Preference'),
                ]
            )
        ]
    )

    # Budget Dropdown
    q.page['left-form-5'] = ui.form_card(
        box='content-left-column',
        title='',
        items=[
            ui.dropdown(
                name='budget',
                label='What’s your budget range per person?',
                value='$500 - $1000',
                choices=[
                    ui.choice(name='<$500', label='<$500'),
                    ui.choice(name='$500 - $1000', label='$500 - $1000'),
                    ui.choice(name='$1000 - $2000', label='$1000 - $2000'),
                    ui.choice(name='$2000 - $4000', label='$2000 - $4000'),
                    ui.choice(name='$4000+', label='$4000+'),
                ]
            )
        ]
    )

    # Accommodation Choice Group
    q.page['left-form-6'] = ui.form_card(
        box='content-left-column',
        title='',
        items=[
            ui.choice_group(
                name='accommodation',
                label='Preferred accommodation type:',
                value='Hotels',
                inline=True,
                choices=[
                    ui.choice(name='Hotels', label='Hotels'),
                    ui.choice(name='Hostels', label='Hostels'),
                    ui.choice(name='Resorts', label='Resorts'),
                    ui.choice(name='Airbnb', label='Airbnb'),
                    ui.choice(name='Camping', label='Camping'),
                ]
            )
        ]
    )
    
    q.page['left-form-button'] = ui.form_card(
        box="content-left-column",
        title="",
        items=[
             ui.buttons(
            items=[ui.button(name="submit", label="Generate",primary=True)],
            justify='center'
        )
        ]
    )

    # Right Column (dummy placeholder)
    q.page['right'] = ui.form_card(
        box="content-right-column",
        title="Left Column",
        items=[ui.button(name='name', label=q.client.themeNameText)]
    )

    q.page['footer'] = ui.form_card(
    box='footer',
    title='',
    items=[
        ui.text(content='''<center><span style="color:gray;">Made with 💛 by Nipun Weerasinghe • 
        <a href="https://www.linkedin.com/in/nipunweerasinghe/" target="_blank" style="color:#1e90ff;">LinkedIn</a></span></center>''')
    ]
)


    await q.page.save()
