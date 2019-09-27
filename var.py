#!/usr/bin/env python

# variables:

query = {'@BernieSanders': 'Bernie Sanders',     # Bernie
         '@ewarren':       'Elizabeth Warren',   # Elizabeth
         '@KamalaHarris':  'Kamala Harris',      # Kamala
         '@PeteButtigieg': 'Pete Buttigieg',     # Pete
         '@JoeBiden':      'Joe Biden',          # Joe Biden
         }

query = dict((k.lower(), v.lower()) for k,v in query.items())

# make everything lowercase for consitency
mentions = list(query.keys())
names = list(query.values())



