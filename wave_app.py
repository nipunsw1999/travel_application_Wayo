from h2o_wave import main, app, Q, ui
import pycountry
from functions import chatWithH2OGPTE_travel,prompt,chatWithH2OGPTE_meal, meal,generate_search_query_from_prompt, getInformationCSV, generate_travel_plan, generate_meal_plan,encode_image_to_base64
import pandas as pd

choices = [ui.choice(name=country.name, label=country.name) for country in pycountry.countries]
restrictions = ['Vegetarian', 'Vegan', 'Gluten Free', 'Halal', 'Kosher']
travel_styles = [
    "Nature", "Adventure", "Beach", "Culture & History", "Luxury",
    "Budget", "Food & Drink", "Nightlife", "Wellness & Spa", "Shopping"
]

base64_image = encode_image_to_base64("static/logo.png")
image_data_uri = f"data:image/jpeg;base64,{base64_image}"

@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        q.client.themeArg = True
        q.client.themeName = 'default'
        q.client.themeNameText = 'Dark'
        q.client.initialized = True
        q.client.restrictions = []
        q.client.travel_plan = ""
        q.client.meal_plan = ""
        q.client.tab = "travel"
        q.client.hasResult = False
        q.client.refI = []


    if q.args.theme:
        q.client.themeArg = not q.client.themeArg

    q.client.themeName = 'default' if q.client.themeArg else 'h2o-dark'
    q.client.themeNameText = 'Dark Mode' if q.client.themeArg else 'Light Mode'


    q.page['meta'] = ui.meta_card(
        box='',
        theme=q.client.themeName,
        layouts=[
            # Mobile / XS layout
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone(name='header'),
                    ui.zone(
                        name='content',
                        direction=ui.ZoneDirection.COLUMN,
                        size='1',
                        zones=[
                            ui.zone(name='content-left', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone(name='content-left-column', direction=ui.ZoneDirection.COLUMN)
                            ]),
                            ui.zone(name='content-right', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone(name='content-right-column-top', direction=ui.ZoneDirection.ROW, size='100px'),
                                ui.zone(name='content-right-column', direction=ui.ZoneDirection.COLUMN, size='1')
                            ])
                        ]
                    ),
                    ui.zone(name='footer', size='80px'),
                ]
            ),
            ui.layout(
                breakpoint='l',
                zones=[
                    ui.zone(name='header'),
                    ui.zone(
                        name='content',
                        direction=ui.ZoneDirection.ROW,
                        size='1',
                        zones=[
                            ui.zone(
                                name='content-left',
                                direction=ui.ZoneDirection.COLUMN,
                                size='50%',
                                zones=[
                                    ui.zone(name='content-left-column', direction=ui.ZoneDirection.COLUMN)
                                ]
                            ),
                            ui.zone(
                                name='content-right',
                                direction=ui.ZoneDirection.COLUMN,
                                size='50%',
                                zones=[
                                    ui.zone(name='content-right-column-top', direction=ui.ZoneDirection.ROW, size='100px'),
                                    ui.zone(name='content-right-column', direction=ui.ZoneDirection.COLUMN, size='1')
                                ]
                            )
                        ]
                    ),
                    ui.zone(name='footer', size='80px')
                ]
            )
        ]
    )




    q.page['header'] = ui.header_card(
        box='header',
        title='Wayo',
        subtitle='LLM powered by H2O Wave',
        image=image_data_uri,
        items=[ui.button(name='theme', label=q.client.themeNameText)]
        )

    q.page['footer'] = ui.form_card(
        box='footer',
        title='',
        items=[ui.text(content='''<center><span style="color:gray;">Made with 💛 by Nipun Weerasinghe • 
        <a href="https://www.linkedin.com/in/nipunweerasinghe/" target="_blank" style="color:#1e90ff;">LinkedIn</a></span></center>''')]
    )

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
    
    q.page['left-form-3'] = ui.form_card(
        box='content-left-column',
        title='',
        items=[ui.checklist(name='travel_styles', label='What kind of experiences are you looking for?', inline=True,
                            choices=[ui.choice(name=style, label=style) for style in travel_styles])]
    )

    q.page['left-form-4'] = ui.form_card(
        box="content-left-column",
        title='',
        items=[ui.checklist(name='meal_preferences', label='Do you have any meal preferences?', inline=True, values=[], choices=[
            ui.choice(name='Vegetarian', label='Vegetarian'),
            ui.choice(name='Vegan', label='Vegan'),
            ui.choice(name='Gluten-Free', label='Gluten-Free'),
            ui.choice(name='Halal', label='Halal'),
            ui.choice(name='Kosher', label='Kosher'),
            ui.choice(name='Seafood', label='Seafood'),
            ui.choice(name='Local Cuisine', label='Local Cuisine'),
            ui.choice(name='No Preference', label='No Preference'),
        ])]
    )

    q.page['left-form-5'] = ui.form_card(
        box='content-left-column',
        title='',
        items=[ui.dropdown(name='budget', label='What’s your budget range per person?', value='$500 - $1000', choices=[
            ui.choice(name='<$500', label='<$500'),
            ui.choice(name='$500 - $1000', label='$500 - $1000'),
            ui.choice(name='$1000 - $2000', label='$1000 - $2000'),
            ui.choice(name='$2000 - $4000', label='$2000 - $4000'),
            ui.choice(name='$4000+', label='$4000+'),
        ])]
    )

    q.page['left-form-6'] = ui.form_card(
        box='content-left-column',
        title='',
        items=[ui.choice_group(name='accommodation', label='Preferred accommodation type:', value='Hotels', inline=True, choices=[
            ui.choice(name='Hotels', label='Hotels'),
            ui.choice(name='Hostels', label='Hostels'),
            ui.choice(name='Resorts', label='Resorts'),
            ui.choice(name='Airbnb', label='Airbnb'),
            ui.choice(name='Camping', label='Camping'),
        ])]
    )

    q.page['left-form-button'] = ui.form_card(
        box="content-left-column",
        title="",
        items=[ui.buttons(items=[ui.button(name="gen", label="Generate", primary=True)], justify='center')]
    )



    if q.args.gen:
        q.client.hasResult = False
        q.client.refI = []
        del q.page['form-right-tabs']
        del q.page['form-right-content-meal']
        del q.page['form-right-content-reference']
        del q.page['form-right-content-travel']
        q.page['example1'] = ui.form_card(
            box='content-right-column',
            items=[ui.progress(label='Planning Your Dream Trip...', caption='Sit tight, your journey is being planned!')]
        )
        await q.page.save()

        travel_prompt = prompt(q.args.member_count, q.args.selected_countries, q.args.trip_days, q.args.budget, q.args.accommodation, q.args.travel_styles, q.args.meal_preferences)
        meal_prompt = meal(q.args.member_count, q.args.selected_countries, q.args.trip_days, q.args.meal_preferences)

        sub_prompt = generate_search_query_from_prompt(travel_prompt)
        getInformationCSV(sub_prompt)

        q.client.travel_plan = chatWithH2OGPTE_travel(travel_prompt)
        q.client.meal_plan = chatWithH2OGPTE_meal(meal_prompt)
        q.client.hasResult = True
        del q.page['example1']
        
    if q.client.hasResult:
        # Tabs
        q.page['form-right-tabs'] = ui.form_card(
            box='content-right-column-top',
            items=[
                ui.tabs(name='tab', value=q.client.tab, items=[
                    ui.tab(name='travel', label='Travel Plan'),
                    ui.tab(name='meal', label='Meal Plan'),
                    ui.tab(name='reference', label='Reference'),
                ])
            ]
        )

        # Tab selection handling
        if q.args.tab:
            q.client.tab = q.args.tab

        # Conditional rendering based on selected tab
        if q.client.tab == "travel":
            
            del q.page['form-right-content-meal']
            del q.page['form-right-content-reference']
            for i in q.client.refI:
                del q.page[f'form-right-content-reference{i}']
                
            q.page['form-right-content-travel'] = ui.form_card(
                box='content-right-column',
                title='Travel Plan',
                items=[ui.text(q.client.travel_plan)]
            )
        elif q.client.tab == "meal":
            
            del q.page['form-right-content-travel']
            del q.page['form-right-content-reference']
            for i in q.client.refI:
                del q.page[f'form-right-content-reference{i}']
                
            q.page['form-right-content-meal'] = ui.form_card(
                box='content-right-column',
                title='Meal Plan',
                items=[ui.text(q.client.meal_plan)]
            )


        elif q.client.tab == "reference":
            import pandas as pd

            df = pd.read_csv("Data Source/travel_search_results.csv")
            image_column = df.columns[-1]

            # Clean up previous tab content safely
            del q.page['form-right-content-travel']
            del q.page['form-right-content-meal']

            for i, row in df.iterrows():
                q.client.refI.append(i)
                title = row["Title"]
                link = row["Link"]
                image_url = row[image_column]

                if pd.notna(image_url) and image_url.startswith(('http://', 'https://', '//')) and not image_url.startswith("x-raw-image://"):
                    if image_url.startswith('//'):
                        image_url = 'https:' + image_url

                    q.page[f"form-right-content-reference{i}"] = ui.form_card(
                        box='content-right-column',
                        title=title,
                        items=[
                            ui.text(f'[View Source]({link})'),ui.image(title=title, path=image_url,width='300px'),
                        ]
                    )



    await q.page.save()
