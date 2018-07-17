#!/usr/bin/python
# -*- coding:utf-8 -*-
from sh_house_data.app import create_app

config_name = 'development'
app = create_app(config_name)


if __name__ == '__main__':
    app.logger.info('app run...')
    app.run()