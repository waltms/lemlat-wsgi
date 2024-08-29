# LEMLAT3 with WSGI

This is a short and simple WSGI web interface for LEMLAT3, a product of the [CIRCSE Research Centre](https://centridiricerca.unicatt.it/circse/it.html). In order to use this, you will need a running copy of LEMLAT3, which can be found [here](https://github.com/CIRCSE/LEMLAT3?tab=readme-ov-file). This interface was specifically written to use the precompiled embedded `lemlat` in `bin/linux_embedded/` of the LEMLAT3 package, but you should be able to get it to work with the non-embedded version.

## Installation

 - Your webserver must have WSGI enabled. In the appropriate web directory (e.g. `/var/www/wsgi/lemlat/`) copy your entire `bin/linux_embedded/` contents from the LEMLAT3 download.
 - Copy `lemlat.py` and `lemlat.html` from this repository into the same directory.
 - Add the following directives into your webserver config file:

```apacheconf
    <Directory "/var/www/wsgi/lemlat">
        Require all granted
    </Directory>

    WSGIScriptAlias /lemlat /var/www/wsgi/lemlat/lemlat.py
```

 - Restart your webserver.

## Usage

The web interface should now be usable as: `https://my-web-site/lemlat?word=bellum`

The results resemble standard LEMLAT3 output, with minimal styling.

>[!NOTE]
>Lemmas have a link to the corresponding entries in [Logeion](https://logeion.uchicago.edu/).

>[!TIP]
>In `lemlat.py` there are two variables worthy of being mentioned. One is `acceptable_referers`, a list of acceptable referers, in case you would like the interface to only be accessible from a pre-designated website link. This functionality will only be enforced if the variable `need_referer` is set to `True`.
