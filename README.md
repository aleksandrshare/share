## examples only
## not for run  

pip install -r requirements.txt

### architecture
```
framework
    api_libs - client for api
    ui_libs - client for selenium
    platform
        api_auto - extends api_libs
    other_proj_ui 
        ui_auto - extends ui_libs and locators
tests
    fixtures - initialize workers classes and other func
```
     
    