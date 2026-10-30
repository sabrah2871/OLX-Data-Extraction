# OLX-Data-Extraction
## Extract data from OLX website
Making list of **rental house and apartment which located in Jatinegara, East Jakarta**.  Data is taken and extracted from OLX [website](https://www.olx.co.id), with the use of Python Scrapy library.

Project structure:
```
.
├── olx
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       └── olxspider.py
├── olxjatinegara.json
├── README.MD
└── scrapy.cfg
```
All files and folders (except `README.MD`, `olxspider.py` and `olxjatinegara.json`) are generated through CLI
`scrapy startproject olx`.

`olxspider.py` is generated through CLI `scrapy genspider olxspider`.

For this project we make use of `olxspider.py` and `settings.py` and keep untouched the other ones.
After updating code and some setting in `olxspider.py` and `settings.py` run CLI `scrapy crawl olxjatinegara.json` to obtain the list of rental house and apartment in Jatinegara, East Jakarta.
