from h2o_wave import main, app, Q, ui

@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        q.client.themeArg = True
        q.client.themeName = 'default'
        q.client.themeNameText = 'Dark'
        q.client.initialized = True

    if q.args.theme:
        q.client.themeArg = not q.client.themeArg

    if q.client.themeArg:
        q.client.themeName = 'default'
        q.client.themeNameText = 'Dark'
    else:
        q.client.themeName = 'h2o-dark'
        q.client.themeNameText = 'Light'

    q.page['meta'] = ui.meta_card(
        box='',
        theme=q.client.themeName,
        layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone(name='header'),
                    ui.zone(name='content',direction=ui.ZoneDirection.ROW, size='100%',
                            zones=[
                                    ui.zone(name="content-left",direction=ui.ZoneDirection.COLUMN, size='50%',
                                            zones=[
                                                    ui.zone(name="content-left-column",direction=ui.ZoneDirection.COLUMN)
                                                ]),
                                    ui.zone(name="content-right",direction=ui.ZoneDirection.COLUMN, size='50%',
                                            zones=[
                                                    ui.zone(name="content-right-column",direction=ui.ZoneDirection.COLUMN)
                                                ]),
                                ]),
                    ui.zone(name='footer'),
                ]
            )
        ]
    )

    q.page['header'] = ui.header_card(
        box='header',
        title='Wayo',
        subtitle='LLM powered by H2O Wave',
        image='https://wave.h2o.ai/img/h2o-logo.svg',
        items=[
            ui.button(name='theme', label=q.client.themeNameText),
        ]
    )

    q.page['left'] = ui.form_card(
        box="content-left-column",
        title="Left Column",
        items=[
            ui.button(name='name', label=q.client.themeNameText),
            ]
    )
    
    q.page['right'] = ui.form_card(
        box="content-right-column",
        title="Left Column",
        items=[
            ui.button(name='name', label=q.client.themeNameText),
            ]
    )
    await q.page.save()
