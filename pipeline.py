from price_update import YandexMarketUpdater

# Samsung:
updater_samsung = YandexMarketUpdater(
    spreadsheet_url="https://docs.google.com/spreadsheets/d/1-0fSX404BKuzZRCgVflyNT-4icIDOnmF4cyaHdkrz6Y/edit",
    credentials_file="credentials.json",
    oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
    business_id="198575908"
)

# Android:
updater_android = YandexMarketUpdater(
    spreadsheet_url="https://docs.google.com/spreadsheets/d/1GlSldh85vf2SBDzeDE1ote5ojc8UcysdbU9Yi83Cw1w/edit?usp=sharing",
    credentials_file="credentials.json",
    oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
    business_id="198575908"
)

# Apple nanoSim+eSim:
updater_apple_nanoSim_eSim = YandexMarketUpdater(
    spreadsheet_url="https://docs.google.com/spreadsheets/d/1tn6Qh3zOjEYvF78ApJ0GkOZcj1_iVdGAXv1KHbAU2Hc/edit?usp=sharing",
    credentials_file="credentials.json",
    oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
    business_id="198575908"
)

# Apple nanoSim+eSim:
updater_apple_eSim = YandexMarketUpdater(
    spreadsheet_url="https://docs.google.com/spreadsheets/d/1A0mW5Xj4Jc1Ystt3XrsecX9sZtg3Ad-z7V0Y_emZtTU/edit?usp=sharing",
    credentials_file="credentials.json",
    oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
    business_id="198575908"
)

# Apple MacBook:
update_macbook = YandexMarketUpdater(
    spreadsheet_url="https://docs.google.com/spreadsheets/d/1xDQaCrXEoI1Fb3eNEhk8UbFTgT9qtFDtn-TF8axUUXo/edit?usp=sharing",
    credentials_file="credentials.json",
    oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
    business_id="198575908"
)

# Update DJI
update_dji = YandexMarketUpdater(
spreadsheet_url="https://docs.google.com/spreadsheets/d/1AcA5iNUl9NFplSTAislS42PmHyLEepBdTKQVE96ZuAI/edit?gid=0#gid=0",
    credentials_file="credentials.json",
    oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
    business_id="198575908"
)

# Update Apple Watch
update_apple_watch = YandexMarketUpdater(
spreadsheet_url="https://docs.google.com/spreadsheets/d/1Ea24Hg9yziuPnv-Vpz5kVXUrFE1uGaIC3cjZyF4IOSg/edit?usp=sharing",
    credentials_file="credentials.json",
    oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
    business_id="198575908"
)


# Запуски:
updater_samsung.run()
updater_android.run()
updater_apple_nanoSim_eSim.run()
updater_apple_eSim.run()
update_macbook.run()
update_dji.run()
update_apple_watch.run()