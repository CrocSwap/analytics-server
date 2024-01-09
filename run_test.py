from gevent import monkey
monkey.patch_all()
import csv
import json
import os
#import subprocess
import gevent.subprocess as subprocess
from gevent import spawn
import time
import unittest
import pprint
import requests
import docker
from common.DataClasses import ServerConfig
from locust import HttpUser, task, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history
import threading
from locust import HttpUser, task, between, events
from locust.env import Environment
from locust.stats import stats_printer
from locust import events                        
import argparse
default_chain_ids = [ "0x1", "0x5"]

terrible_client_request =   {"service":"run","config":"batch_requests","include_data":"0","data":
                             {"req":[{"config_path":"ens_address","req_id":"0x0b98718264ca14d0a17c145ffe1e4f3c38a39372","args":{"config_path":"ens_address","address":"0x0b98718264ca14d0a17c145ffe1e4f3c38a39372"}},{"config_path":"ens_address","req_id":"0x520c7792f2343c7a5c9f230bd39c565918fcf215","args":{"config_path":"ens_address","address":"0x520c7792f2343c7a5c9f230bd39c565918fcf215"}},{"config_path":"ens_address","req_id":"0x425a4a539c085ff2568e19ee1304e97a92688959","args":{"config_path":"ens_address","address":"0x425a4a539c085ff2568e19ee1304e97a92688959"}},{"config_path":"ens_address","req_id":"0x524cfae2daab901234c842f3a17235902b0f01f9","args":{"config_path":"ens_address","address":"0x524cfae2daab901234c842f3a17235902b0f01f9"}},{"config_path":"ens_address","req_id":"0x000000422a649825bda802b2c212c46127bd96fd","args":{"config_path":"ens_address","address":"0x000000422a649825bda802b2c212c46127bd96fd"}},{"config_path":"ens_address","req_id":"0x000000ffa51e8fd8dc15c5b77990234810a640e8","args":{"config_path":"ens_address","address":"0x000000ffa51e8fd8dc15c5b77990234810a640e8"}},{"config_path":"ens_address","req_id":"0xf05c12fa7d8548be726844067a0e63fa6234f0bb","args":{"config_path":"ens_address","address":"0xf05c12fa7d8548be726844067a0e63fa6234f0bb"}},{"config_path":"ens_address","req_id":"0xc9f2e6ea1637e499406986ac50ddc92401ce1f58","args":{"config_path":"ens_address","address":"0xc9f2e6ea1637e499406986ac50ddc92401ce1f58"}},{"config_path":"ens_address","req_id":"0x566cdc415fdf629a47e365b5fdfadce51a2f8752","args":{"config_path":"ens_address","address":"0x566cdc415fdf629a47e365b5fdfadce51a2f8752"}},{"config_path":"ens_address","req_id":"0xf0b8bcd1921d37bf83d71ccee40d55a13b98f3c5","args":{"config_path":"ens_address","address":"0xf0b8bcd1921d37bf83d71ccee40d55a13b98f3c5"}},{"config_path":"ens_address","req_id":"0xe8e14416bc2c76584cbab2709bcb54fa8f7c7c29","args":{"config_path":"ens_address","address":"0xe8e14416bc2c76584cbab2709bcb54fa8f7c7c29"}},{"config_path":"ens_address","req_id":"0x9bf2df3e97a2a181221424ddc14b18400e94f776","args":{"config_path":"ens_address","address":"0x9bf2df3e97a2a181221424ddc14b18400e94f776"}},{"config_path":"ens_address","req_id":"0x7bde9f12a8b64b2c83b80ab7d9e3ec53e3146f1a","args":{"config_path":"ens_address","address":"0x7bde9f12a8b64b2c83b80ab7d9e3ec53e3146f1a"}},{"config_path":"ens_address","req_id":"0x829bbc1f94ee2fa7856e17bb7ab2b8fda6f3bd53","args":{"config_path":"ens_address","address":"0x829bbc1f94ee2fa7856e17bb7ab2b8fda6f3bd53"}},{"config_path":"ens_address","req_id":"0x9523455efa948e878e18892d4299dab442d02533","args":{"config_path":"ens_address","address":"0x9523455efa948e878e18892d4299dab442d02533"}},{"config_path":"ens_address","req_id":"0xcb1141e9ddb6858cdb4b2e622cb4ac762af66013","args":{"config_path":"ens_address","address":"0xcb1141e9ddb6858cdb4b2e622cb4ac762af66013"}},{"config_path":"ens_address","req_id":"0x1f93e7c8b9b4f7a592a4ef9d1d4b63b0dcbfe78c","args":{"config_path":"ens_address","address":"0x1f93e7c8b9b4f7a592a4ef9d1d4b63b0dcbfe78c"}},{"config_path":"ens_address","req_id":"0x5afec0de001999766fb883860cae06f5932e6f32","args":{"config_path":"ens_address","address":"0x5afec0de001999766fb883860cae06f5932e6f32"}},{"config_path":"ens_address","req_id":"0x5646889144dbb12fcdff5d644b5b44e7e5a89acc","args":{"config_path":"ens_address","address":"0x5646889144dbb12fcdff5d644b5b44e7e5a89acc"}},{"config_path":"ens_address","req_id":"0x364e2aea672a791eb516999f16f510b92699a98c","args":{"config_path":"ens_address","address":"0x364e2aea672a791eb516999f16f510b92699a98c"}},{"config_path":"ens_address","req_id":"0xab8e0f243838f5e573b2649bc7304afd5fd36446","args":{"config_path":"ens_address","address":"0xab8e0f243838f5e573b2649bc7304afd5fd36446"}},{"config_path":"ens_address","req_id":"0xaac84e8df34f86edeafe037826c0d4a833237013","args":{"config_path":"ens_address","address":"0xaac84e8df34f86edeafe037826c0d4a833237013"}},{"config_path":"ens_address","req_id":"0x5811b5d57cb3f803151768fea0d22046b1ebd65c","args":{"config_path":"ens_address","address":"0x5811b5d57cb3f803151768fea0d22046b1ebd65c"}},{"config_path":"ens_address","req_id":"0x6335a85f615cbbeae940cfcaf13b2eebe797a806","args":{"config_path":"ens_address","address":"0x6335a85f615cbbeae940cfcaf13b2eebe797a806"}},{"config_path":"ens_address","req_id":"0x5d47e5d242a8f66a6286b0a2353868875f5d6068","args":{"config_path":"ens_address","address":"0x5d47e5d242a8f66a6286b0a2353868875f5d6068"}},{"config_path":"ens_address","req_id":"0xe8628a9f7727bcefeab492d601de0a0fb1ab07fc","args":{"config_path":"ens_address","address":"0xe8628a9f7727bcefeab492d601de0a0fb1ab07fc"}},{"config_path":"ens_address","req_id":"0xe37d637409afc26229ff2072a10d507a8e7a7d88","args":{"config_path":"ens_address","address":"0xe37d637409afc26229ff2072a10d507a8e7a7d88"}},{"config_path":"ens_address","req_id":"0xfd3fa9d94eeb4e9889e60e37d0f1fe24ec59f7e1","args":{"config_path":"ens_address","address":"0xfd3fa9d94eeb4e9889e60e37d0f1fe24ec59f7e1"}},{"config_path":"ens_address","req_id":"0x892476bddafc412a09999351e9cc0a180b4a1426","args":{"config_path":"ens_address","address":"0x892476bddafc412a09999351e9cc0a180b4a1426"}},{"config_path":"ens_address","req_id":"0xea06e9f5b4b1b9343ff1ee153ea0af2bf3d96569","args":{"config_path":"ens_address","address":"0xea06e9f5b4b1b9343ff1ee153ea0af2bf3d96569"}},{"config_path":"ens_address","req_id":"0xae395bbae207bbbaeaaead5136e3f266be752a16","args":{"config_path":"ens_address","address":"0xae395bbae207bbbaeaaead5136e3f266be752a16"}},{"config_path":"ens_address","req_id":"0xa2ef0937cd5fe18ca0328bec1e4f1fc6834ff1f9","args":{"config_path":"ens_address","address":"0xa2ef0937cd5fe18ca0328bec1e4f1fc6834ff1f9"}},{"config_path":"ens_address","req_id":"0xd8844b1661e8d7f22eb34feaee49b888be3f7f9b","args":{"config_path":"ens_address","address":"0xd8844b1661e8d7f22eb34feaee49b888be3f7f9b"}},{"config_path":"ens_address","req_id":"0xe74f9211016af21ad247973c371f0cfc2f5a7d5b","args":{"config_path":"ens_address","address":"0xe74f9211016af21ad247973c371f0cfc2f5a7d5b"}},{"config_path":"ens_address","req_id":"0x0f2e45f704270e38d3da035b79006f608b8fcd7f","args":{"config_path":"ens_address","address":"0x0f2e45f704270e38d3da035b79006f608b8fcd7f"}},{"config_path":"ens_address","req_id":"0xbf23ad232e3cf3fb191fc997207ab5f4bf85686c","args":{"config_path":"ens_address","address":"0xbf23ad232e3cf3fb191fc997207ab5f4bf85686c"}},{"config_path":"ens_address","req_id":"0x138f4087af153ad4e7e65c905d949865655f7308","args":{"config_path":"ens_address","address":"0x138f4087af153ad4e7e65c905d949865655f7308"}},{"config_path":"ens_address","req_id":"0x1626255e55b3c8fa14c933646534e9f8726c649a","args":{"config_path":"ens_address","address":"0x1626255e55b3c8fa14c933646534e9f8726c649a"}},{"config_path":"ens_address","req_id":"0x1d8c586c93abd9f0dd21b985060ed1419324b2e3","args":{"config_path":"ens_address","address":"0x1d8c586c93abd9f0dd21b985060ed1419324b2e3"}},{"config_path":"ens_address","req_id":"0x0ef38b5e79e7725629f3177d8f60d8293db7389f","args":{"config_path":"ens_address","address":"0x0ef38b5e79e7725629f3177d8f60d8293db7389f"}},{"config_path":"ens_address","req_id":"0x29d593d60c78510581fc71226ab8c29a076b1e55","args":{"config_path":"ens_address","address":"0x29d593d60c78510581fc71226ab8c29a076b1e55"}},{"config_path":"ens_address","req_id":"0x7d0e7f786c8625b8d50e180bbae59e2a0b070b2b","args":{"config_path":"ens_address","address":"0x7d0e7f786c8625b8d50e180bbae59e2a0b070b2b"}},{"config_path":"ens_address","req_id":"0xc516d10f792b15452cfca3834bf16071cdf9825b","args":{"config_path":"ens_address","address":"0xc516d10f792b15452cfca3834bf16071cdf9825b"}},{"config_path":"ens_address","req_id":"0x1415a15e6a48b32f721ee3446ce928b274670b78","args":{"config_path":"ens_address","address":"0x1415a15e6a48b32f721ee3446ce928b274670b78"}},{"config_path":"ens_address","req_id":"0xf645a8121202cd81314d5c7c72ebd6f51ee83abf","args":{"config_path":"ens_address","address":"0xf645a8121202cd81314d5c7c72ebd6f51ee83abf"}},{"config_path":"ens_address","req_id":"0x9d32ccb03147e88f0d84dcd846e5bceadfa9bdd0","args":{"config_path":"ens_address","address":"0x9d32ccb03147e88f0d84dcd846e5bceadfa9bdd0"}},{"config_path":"ens_address","req_id":"0xc15ab8dd7daeea5f1aa3b56507cac8a877e21b15","args":{"config_path":"ens_address","address":"0xc15ab8dd7daeea5f1aa3b56507cac8a877e21b15"}},{"config_path":"ens_address","req_id":"0xf1ec0d94ed815b702bb177b561ce4d7362ed3383","args":{"config_path":"ens_address","address":"0xf1ec0d94ed815b702bb177b561ce4d7362ed3383"}},{"config_path":"ens_address","req_id":"0xc21a5ee89d306353e065a6dd5779470de395dbac","args":{"config_path":"ens_address","address":"0xc21a5ee89d306353e065a6dd5779470de395dbac"}},{"config_path":"ens_address","req_id":"0x53144384f3425c985ca395fc4474819274252b54","args":{"config_path":"ens_address","address":"0x53144384f3425c985ca395fc4474819274252b54"}},{"config_path":"ens_address","req_id":"0x0360046dcf3e9fcea24036911addbbc7d1d8620b","args":{"config_path":"ens_address","address":"0x0360046dcf3e9fcea24036911addbbc7d1d8620b"}},{"config_path":"ens_address","req_id":"0x7442ecc6c7545001fa111b2536bbc1162b01646f","args":{"config_path":"ens_address","address":"0x7442ecc6c7545001fa111b2536bbc1162b01646f"}},{"config_path":"ens_address","req_id":"0xfaf33e42372ce3e86a8c219af9ef24ccc35ce037","args":{"config_path":"ens_address","address":"0xfaf33e42372ce3e86a8c219af9ef24ccc35ce037"}},{"config_path":"ens_address","req_id":"0xf5c905db6e7d38570c918d18e76cbc36aaf0c291","args":{"config_path":"ens_address","address":"0xf5c905db6e7d38570c918d18e76cbc36aaf0c291"}},{"config_path":"ens_address","req_id":"0xe21428de432217b6939b46ec02d218e87f96a1c2","args":{"config_path":"ens_address","address":"0xe21428de432217b6939b46ec02d218e87f96a1c2"}},{"config_path":"ens_address","req_id":"0x778ee0e49ba8cab805cd4a3a17e61f9e1c8f40ee","args":{"config_path":"ens_address","address":"0x778ee0e49ba8cab805cd4a3a17e61f9e1c8f40ee"}},{"config_path":"ens_address","req_id":"0xd0da87deb5d8c47b0d3006baf2eb717f3c1ba274","args":{"config_path":"ens_address","address":"0xd0da87deb5d8c47b0d3006baf2eb717f3c1ba274"}},{"config_path":"ens_address","req_id":"0xb2a0536b4af0fd5cf60025a4918285c554fc1220","args":{"config_path":"ens_address","address":"0xb2a0536b4af0fd5cf60025a4918285c554fc1220"}},{"config_path":"ens_address","req_id":"0x2ec7c8215417e7bb2dade0588673e2a188790cc8","args":{"config_path":"ens_address","address":"0x2ec7c8215417e7bb2dade0588673e2a188790cc8"}},{"config_path":"ens_address","req_id":"0x64f38526800d406ac92c6e7e35448bb17abe1a0c","args":{"config_path":"ens_address","address":"0x64f38526800d406ac92c6e7e35448bb17abe1a0c"}},{"config_path":"ens_address","req_id":"0xc81d1f24bdc4539b36b3fcb440987caaa27a9341","args":{"config_path":"ens_address","address":"0xc81d1f24bdc4539b36b3fcb440987caaa27a9341"}},{"config_path":"ens_address","req_id":"0x7e730c8561cbc5f454b31fdc923fc36f8968552b","args":{"config_path":"ens_address","address":"0x7e730c8561cbc5f454b31fdc923fc36f8968552b"}},{"config_path":"ens_address","req_id":"0xbad979702a09841a7672fb6e3c12c3368dff2a19","args":{"config_path":"ens_address","address":"0xbad979702a09841a7672fb6e3c12c3368dff2a19"}},{"config_path":"ens_address","req_id":"0x0128f11c5daad5718237b53148d9b38e8209061f","args":{"config_path":"ens_address","address":"0x0128f11c5daad5718237b53148d9b38e8209061f"}},{"config_path":"ens_address","req_id":"0xf6d9dca5b6c22c366c8c96b8ad773202cc804a78","args":{"config_path":"ens_address","address":"0xf6d9dca5b6c22c366c8c96b8ad773202cc804a78"}},{"config_path":"ens_address","req_id":"0xadeac70065d72034748783c53bbb92d7aec56983","args":{"config_path":"ens_address","address":"0xadeac70065d72034748783c53bbb92d7aec56983"}},{"config_path":"ens_address","req_id":"0xa7d763bc1e788904f2e20b91d3c51e47524ba189","args":{"config_path":"ens_address","address":"0xa7d763bc1e788904f2e20b91d3c51e47524ba189"}},{"config_path":"ens_address","req_id":"0x11e0302f9475713829cba8672e2c06567e3b6aa4","args":{"config_path":"ens_address","address":"0x11e0302f9475713829cba8672e2c06567e3b6aa4"}},{"config_path":"ens_address","req_id":"0x4620abc831d29fc5d67e129b11662cf57e6af61c","args":{"config_path":"ens_address","address":"0x4620abc831d29fc5d67e129b11662cf57e6af61c"}},{"config_path":"ens_address","req_id":"0x99c622a03d9db2d720cc52235551e4795b820d3d","args":{"config_path":"ens_address","address":"0x99c622a03d9db2d720cc52235551e4795b820d3d"}},{"config_path":"ens_address","req_id":"0x6532903a7dabddd2f5d52eeb2437ad37fe6f4d9b","args":{"config_path":"ens_address","address":"0x6532903a7dabddd2f5d52eeb2437ad37fe6f4d9b"}},{"config_path":"ens_address","req_id":"0x269f23d2afc144200b35c08eb886a1736bb79b81","args":{"config_path":"ens_address","address":"0x269f23d2afc144200b35c08eb886a1736bb79b81"}},{"config_path":"ens_address","req_id":"0x074ad9ec101d680d480bf70841124d32d8b2664a","args":{"config_path":"ens_address","address":"0x074ad9ec101d680d480bf70841124d32d8b2664a"}},{"config_path":"ens_address","req_id":"0xc4a267b902685667c68c9731969d9844b78301e1","args":{"config_path":"ens_address","address":"0xc4a267b902685667c68c9731969d9844b78301e1"}},{"config_path":"ens_address","req_id":"0x71008de103ea1863a5537616d651333b03084b8e","args":{"config_path":"ens_address","address":"0x71008de103ea1863a5537616d651333b03084b8e"}},{"config_path":"ens_address","req_id":"0x945d5bcda8dcd9cd8b221fd23cf4b6c0e7e50bd5","args":{"config_path":"ens_address","address":"0x945d5bcda8dcd9cd8b221fd23cf4b6c0e7e50bd5"}},{"config_path":"ens_address","req_id":"0x3faf829e523552e4ad01846f605c184bca855e75","args":{"config_path":"ens_address","address":"0x3faf829e523552e4ad01846f605c184bca855e75"}},{"config_path":"ens_address","req_id":"0xfae8241780da57e83e007ab97439abe39a2dfc88","args":{"config_path":"ens_address","address":"0xfae8241780da57e83e007ab97439abe39a2dfc88"}},{"config_path":"ens_address","req_id":"0x30f66e8e9483c278d802e493b4ca62c98a603df7","args":{"config_path":"ens_address","address":"0x30f66e8e9483c278d802e493b4ca62c98a603df7"}},{"config_path":"ens_address","req_id":"0x43a5d9c141125cd67b9268ef28c7c6a9dc15f3c9","args":{"config_path":"ens_address","address":"0x43a5d9c141125cd67b9268ef28c7c6a9dc15f3c9"}},{"config_path":"ens_address","req_id":"0x5edfda7a115584df2912ac1fd55197079e060fe8","args":{"config_path":"ens_address","address":"0x5edfda7a115584df2912ac1fd55197079e060fe8"}},{"config_path":"ens_address","req_id":"0xa1457afa30b8e396cde5bac320ed7c8e7b521bc8","args":{"config_path":"ens_address","address":"0xa1457afa30b8e396cde5bac320ed7c8e7b521bc8"}},{"config_path":"ens_address","req_id":"0x7e33dbdc4cf728a8b06c2cdab2c8b41195fde83c","args":{"config_path":"ens_address","address":"0x7e33dbdc4cf728a8b06c2cdab2c8b41195fde83c"}},{"config_path":"ens_address","req_id":"0xa611d8b0feee7230bb27875923d71328134d8277","args":{"config_path":"ens_address","address":"0xa611d8b0feee7230bb27875923d71328134d8277"}},{"config_path":"ens_address","req_id":"0x91dda995be3a56bbf2ac6e5e14eb9213a336aac6","args":{"config_path":"ens_address","address":"0x91dda995be3a56bbf2ac6e5e14eb9213a336aac6"}},{"config_path":"ens_address","req_id":"0xf88353e6b33d1f9f6f325dbcbb697ddd0be3bd5c","args":{"config_path":"ens_address","address":"0xf88353e6b33d1f9f6f325dbcbb697ddd0be3bd5c"}},{"config_path":"ens_address","req_id":"0xf8c9b9c9a95a6cd6a86fac95dd3a09abe6c6a60e","args":{"config_path":"ens_address","address":"0xf8c9b9c9a95a6cd6a86fac95dd3a09abe6c6a60e"}},{"config_path":"ens_address","req_id":"0x9390537c031b3f53c5982a8f40821602ffe3b28e","args":{"config_path":"ens_address","address":"0x9390537c031b3f53c5982a8f40821602ffe3b28e"}},{"config_path":"ens_address","req_id":"0x3eefd8089cddd8d550324b37a8d881cf8aa9fd46","args":{"config_path":"ens_address","address":"0x3eefd8089cddd8d550324b37a8d881cf8aa9fd46"}},{"config_path":"ens_address","req_id":"0xbc2c77d7d4742a7209503e0820de27117b843b1f","args":{"config_path":"ens_address","address":"0xbc2c77d7d4742a7209503e0820de27117b843b1f"}},{"config_path":"ens_address","req_id":"0x9c39888f6ebec9c286f59c5219e869464ed11569","args":{"config_path":"ens_address","address":"0x9c39888f6ebec9c286f59c5219e869464ed11569"}},{"config_path":"ens_address","req_id":"0x2ce1fce87781b3c70b181cd575876d4a42324774","args":{"config_path":"ens_address","address":"0x2ce1fce87781b3c70b181cd575876d4a42324774"}},{"config_path":"ens_address","req_id":"0xb255270e12b58042044eaf7ba2bccd60d738dd4b","args":{"config_path":"ens_address","address":"0xb255270e12b58042044eaf7ba2bccd60d738dd4b"}},{"config_path":"ens_address","req_id":"0x478ce50d3ce95224312a3f44ade1e3ddc047ae1a","args":{"config_path":"ens_address","address":"0x478ce50d3ce95224312a3f44ade1e3ddc047ae1a"}},{"config_path":"ens_address","req_id":"0x25fc90175907d2144171ac2752ac009f05c2aaf2","args":{"config_path":"ens_address","address":"0x25fc90175907d2144171ac2752ac009f05c2aaf2"}},{"config_path":"ens_address","req_id":"0xca9ba74ee20917211ef646ac51accc287f27538b","args":{"config_path":"ens_address","address":"0xca9ba74ee20917211ef646ac51accc287f27538b"}},{"config_path":"ens_address","req_id":"0x7bfee91193d9df2ac0bfe90191d40f23c773c060","args":{"config_path":"ens_address","address":"0x7bfee91193d9df2ac0bfe90191d40f23c773c060"}},{"config_path":"ens_address","req_id":"0x2f2f665974261c4129b1dc6c359bd259cd66f78a","args":{"config_path":"ens_address","address":"0x2f2f665974261c4129b1dc6c359bd259cd66f78a"}},{"config_path":"ens_address","req_id":"0xfbbced3bf2f503dd19800f595bb61a3660e108a6","args":{"config_path":"ens_address","address":"0xfbbced3bf2f503dd19800f595bb61a3660e108a6"}},{"config_path":"ens_address","req_id":"0x1853e5df825514689a4195714df85e54af7d7b76","args":{"config_path":"ens_address","address":"0x1853e5df825514689a4195714df85e54af7d7b76"}},{"config_path":"ens_address","req_id":"0xd88cac7ee406e5aecdf3124d21eea03e886c6dbd","args":{"config_path":"ens_address","address":"0xd88cac7ee406e5aecdf3124d21eea03e886c6dbd"}},{"config_path":"ens_address","req_id":"0xaba92f62ef9d45d0b61808d330461c3b2d8fece8","args":{"config_path":"ens_address","address":"0xaba92f62ef9d45d0b61808d330461c3b2d8fece8"}},{"config_path":"ens_address","req_id":"0x465b1e44b9a346240ebdd64101e93d8275ee4446","args":{"config_path":"ens_address","address":"0x465b1e44b9a346240ebdd64101e93d8275ee4446"}},{"config_path":"ens_address","req_id":"0x926524a86c29b7c6b789257720b2c5d287faf942","args":{"config_path":"ens_address","address":"0x926524a86c29b7c6b789257720b2c5d287faf942"}},{"config_path":"ens_address","req_id":"0xb6d36381f5944325e58b62fa6cee22342ea0d795","args":{"config_path":"ens_address","address":"0xb6d36381f5944325e58b62fa6cee22342ea0d795"}},{"config_path":"ens_address","req_id":"0x16224283be3f7c0245d9d259ea82ead7fcb8343d","args":{"config_path":"ens_address","address":"0x16224283be3f7c0245d9d259ea82ead7fcb8343d"}},{"config_path":"ens_address","req_id":"0x0a1245f97f3a7305a668a5cce5f9c2095ea719a7","args":{"config_path":"ens_address","address":"0x0a1245f97f3a7305a668a5cce5f9c2095ea719a7"}},{"config_path":"ens_address","req_id":"0xb48780c41f6f00e4efd3bba686c2acabe4b9dcb1","args":{"config_path":"ens_address","address":"0xb48780c41f6f00e4efd3bba686c2acabe4b9dcb1"}},{"config_path":"ens_address","req_id":"0xd4d823fe41fded38d458ea55e953537b7a9bbe34","args":{"config_path":"ens_address","address":"0xd4d823fe41fded38d458ea55e953537b7a9bbe34"}},{"config_path":"ens_address","req_id":"0xf951cc0932d33d35f1a9282d0f3df540cf923dd9","args":{"config_path":"ens_address","address":"0xf951cc0932d33d35f1a9282d0f3df540cf923dd9"}},{"config_path":"ens_address","req_id":"0xeb91386f351903d132a8abf44a3d82903bf27e92","args":{"config_path":"ens_address","address":"0xeb91386f351903d132a8abf44a3d82903bf27e92"}},{"config_path":"ens_address","req_id":"0x1ea2a806f60d3abd361b2e9ec992ba7b85258343","args":{"config_path":"ens_address","address":"0x1ea2a806f60d3abd361b2e9ec992ba7b85258343"}},{"config_path":"ens_address","req_id":"0xb8c327d17b08f0aea542bd61a471ae3533b37750","args":{"config_path":"ens_address","address":"0xb8c327d17b08f0aea542bd61a471ae3533b37750"}},{"config_path":"ens_address","req_id":"0x8de17b7fc6b553bc25269d75f09ead21a9259a6c","args":{"config_path":"ens_address","address":"0x8de17b7fc6b553bc25269d75f09ead21a9259a6c"}},{"config_path":"ens_address","req_id":"0x710dc8c61b177687f1e3c085f694896cdc438209","args":{"config_path":"ens_address","address":"0x710dc8c61b177687f1e3c085f694896cdc438209"}},{"config_path":"ens_address","req_id":"0xbf631520425edb5e474278e1d97b86bd76c1de70","args":{"config_path":"ens_address","address":"0xbf631520425edb5e474278e1d97b86bd76c1de70"}},{"config_path":"ens_address","req_id":"0xe3ed0806b6adb484bedfbd350fe84bed92a13d0d","args":{"config_path":"ens_address","address":"0xe3ed0806b6adb484bedfbd350fe84bed92a13d0d"}},{"config_path":"ens_address","req_id":"0xf15d680449acc526578ce6c466e0f44010d89b64","args":{"config_path":"ens_address","address":"0xf15d680449acc526578ce6c466e0f44010d89b64"}},{"config_path":"ens_address","req_id":"0x6db3ebedc8e67afe3f8d3c3f001ff3d691182f21","args":{"config_path":"ens_address","address":"0x6db3ebedc8e67afe3f8d3c3f001ff3d691182f21"}},{"config_path":"ens_address","req_id":"0xa07959a45a5d14e005465b09e50b792672644282","args":{"config_path":"ens_address","address":"0xa07959a45a5d14e005465b09e50b792672644282"}},{"config_path":"ens_address","req_id":"0x5f73160fa1ed2617ca44cc080522a211977d27aa","args":{"config_path":"ens_address","address":"0x5f73160fa1ed2617ca44cc080522a211977d27aa"}},{"config_path":"ens_address","req_id":"0x1bda0a00d113eee140757aa5603c7cca15295153","args":{"config_path":"ens_address","address":"0x1bda0a00d113eee140757aa5603c7cca15295153"}},{"config_path":"ens_address","req_id":"0xf756a2be397e37b5513b44192e0ec4c880d20ea2","args":{"config_path":"ens_address","address":"0xf756a2be397e37b5513b44192e0ec4c880d20ea2"}},{"config_path":"ens_address","req_id":"0x1649b26eae366218f774286c38a167c1c69afeca","args":{"config_path":"ens_address","address":"0x1649b26eae366218f774286c38a167c1c69afeca"}},{"config_path":"ens_address","req_id":"0xcb80b353c4a5a1d084d8f3c3b86562c8c3a56ac8","args":{"config_path":"ens_address","address":"0xcb80b353c4a5a1d084d8f3c3b86562c8c3a56ac8"}},{"config_path":"ens_address","req_id":"0xbc6d3a411d4fb11c17c644ae374d59bbac61d5df","args":{"config_path":"ens_address","address":"0xbc6d3a411d4fb11c17c644ae374d59bbac61d5df"}},{"config_path":"ens_address","req_id":"0x6ffc40e41897421f381abf343301fdd01cccec34","args":{"config_path":"ens_address","address":"0x6ffc40e41897421f381abf343301fdd01cccec34"}},{"config_path":"ens_address","req_id":"0x8da0a5f9dd8ad28298041835259281ce05feaf3c","args":{"config_path":"ens_address","address":"0x8da0a5f9dd8ad28298041835259281ce05feaf3c"}},{"config_path":"ens_address","req_id":"0x6adcf08deaaf5913079707f923279ef4c6d5225e","args":{"config_path":"ens_address","address":"0x6adcf08deaaf5913079707f923279ef4c6d5225e"}},{"config_path":"ens_address","req_id":"0x6e82554d7c496baccc8d0bcb104a50b772d22a1f","args":{"config_path":"ens_address","address":"0x6e82554d7c496baccc8d0bcb104a50b772d22a1f"}},{"config_path":"ens_address","req_id":"0x08ab4e5199a5e8bd9575bba899a9561a7cfe8fd6","args":{"config_path":"ens_address","address":"0x08ab4e5199a5e8bd9575bba899a9561a7cfe8fd6"}},{"config_path":"ens_address","req_id":"0x04c18cbf703c72591f1800b52d801a948f55e00c","args":{"config_path":"ens_address","address":"0x04c18cbf703c72591f1800b52d801a948f55e00c"}},{"config_path":"ens_address","req_id":"0xfbd6bc610d64e3bd34e7b1701c9e0a9a8d56dd16","args":{"config_path":"ens_address","address":"0xfbd6bc610d64e3bd34e7b1701c9e0a9a8d56dd16"}},{"config_path":"ens_address","req_id":"0x1aaf5e41c2c73617bc120097547a3410caf6718a","args":{"config_path":"ens_address","address":"0x1aaf5e41c2c73617bc120097547a3410caf6718a"}},{"config_path":"ens_address","req_id":"0x322007c5e17d7992cd139f09460c9c17c24216bf","args":{"config_path":"ens_address","address":"0x322007c5e17d7992cd139f09460c9c17c24216bf"}},{"config_path":"ens_address","req_id":"0x24a4ff5273c91a47ee830b25bbbe5d7d3fe47e5d","args":{"config_path":"ens_address","address":"0x24a4ff5273c91a47ee830b25bbbe5d7d3fe47e5d"}},{"config_path":"ens_address","req_id":"0x435a675c73c7bafe1f28ce128205cf4387972c92","args":{"config_path":"ens_address","address":"0x435a675c73c7bafe1f28ce128205cf4387972c92"}},{"config_path":"ens_address","req_id":"0xc0c44b69d91ea0b26f5be8afedc18a8cee281ad7","args":{"config_path":"ens_address","address":"0xc0c44b69d91ea0b26f5be8afedc18a8cee281ad7"}},{"config_path":"ens_address","req_id":"0xd6431f624e2d5a24686ac6bdaed34a978da23f15","args":{"config_path":"ens_address","address":"0xd6431f624e2d5a24686ac6bdaed34a978da23f15"}},{"config_path":"ens_address","req_id":"0x55e1490a1878d0b61811726e2cb96560022e764c","args":{"config_path":"ens_address","address":"0x55e1490a1878d0b61811726e2cb96560022e764c"}},{"config_path":"ens_address","req_id":"0xd9d836ebc67abeec65b29e586f89816dab991f69","args":{"config_path":"ens_address","address":"0xd9d836ebc67abeec65b29e586f89816dab991f69"}},{"config_path":"ens_address","req_id":"0x8a88dfcc83c2999a81634899f55512a88d0d84b2","args":{"config_path":"ens_address","address":"0x8a88dfcc83c2999a81634899f55512a88d0d84b2"}},{"config_path":"ens_address","req_id":"0x4454e740ff1c31faafaf77b04f20fa6de0cbd0ca","args":{"config_path":"ens_address","address":"0x4454e740ff1c31faafaf77b04f20fa6de0cbd0ca"}},{"config_path":"ens_address","req_id":"0x2bc55eae1c5c5ff8d4ed79b1eac06a4d350a7c91","args":{"config_path":"ens_address","address":"0x2bc55eae1c5c5ff8d4ed79b1eac06a4d350a7c91"}},{"config_path":"ens_address","req_id":"0x714cd8718adc069bf23119c70b7dc093ad949e8f","args":{"config_path":"ens_address","address":"0x714cd8718adc069bf23119c70b7dc093ad949e8f"}},{"config_path":"ens_address","req_id":"0x900d1719363e97176cbe2274cc4483245ad3270e","args":{"config_path":"ens_address","address":"0x900d1719363e97176cbe2274cc4483245ad3270e"}},{"config_path":"ens_address","req_id":"0x06427ae8972e78bd5bf3706eb98919188d55738f","args":{"config_path":"ens_address","address":"0x06427ae8972e78bd5bf3706eb98919188d55738f"}},{"config_path":"ens_address","req_id":"0x85f131af9666d8cd8fe8fa900a8cb456e9e24361","args":{"config_path":"ens_address","address":"0x85f131af9666d8cd8fe8fa900a8cb456e9e24361"}},{"config_path":"ens_address","req_id":"0x5839bf03e9c7936123db1d3998d3f88efa808c89","args":{"config_path":"ens_address","address":"0x5839bf03e9c7936123db1d3998d3f88efa808c89"}},{"config_path":"ens_address","req_id":"0x00897e2d7168165b81558c3cd9257efb007f2410","args":{"config_path":"ens_address","address":"0x00897e2d7168165b81558c3cd9257efb007f2410"}},{"config_path":"ens_address","req_id":"0x67691771270f0199bfe54a00f8343d15afc5b872","args":{"config_path":"ens_address","address":"0x67691771270f0199bfe54a00f8343d15afc5b872"}},{"config_path":"ens_address","req_id":"0x5f44fe1c8b5d0802eda2a9b638c6163ad52d633b","args":{"config_path":"ens_address","address":"0x5f44fe1c8b5d0802eda2a9b638c6163ad52d633b"}},{"config_path":"ens_address","req_id":"0xb64fcbddb632c0420784b325e51766a97dcc8023","args":{"config_path":"ens_address","address":"0xb64fcbddb632c0420784b325e51766a97dcc8023"}},{"config_path":"ens_address","req_id":"0x5ecd8224c8b40a0df781719c9feffdcc6677e521","args":{"config_path":"ens_address","address":"0x5ecd8224c8b40a0df781719c9feffdcc6677e521"}},{"config_path":"ens_address","req_id":"0x3a631b481a1b225e32d20c28bb531587e9f32da0","args":{"config_path":"ens_address","address":"0x3a631b481a1b225e32d20c28bb531587e9f32da0"}},{"config_path":"ens_address","req_id":"0x4f48855332d27cb1ac94bb4b94e7f96f50a39483","args":{"config_path":"ens_address","address":"0x4f48855332d27cb1ac94bb4b94e7f96f50a39483"}},{"config_path":"ens_address","req_id":"0x05783022615f76de7e887aed81307ae39206aa95","args":{"config_path":"ens_address","address":"0x05783022615f76de7e887aed81307ae39206aa95"}},{"config_path":"ens_address","req_id":"0x7ced2a1a6e97eeae67866c76857dc76a3b28ed01","args":{"config_path":"ens_address","address":"0x7ced2a1a6e97eeae67866c76857dc76a3b28ed01"}},{"config_path":"ens_address","req_id":"0x1bdd5bc3a4c0f550251033cb7575b87811ec94d1","args":{"config_path":"ens_address","address":"0x1bdd5bc3a4c0f550251033cb7575b87811ec94d1"}},{"config_path":"ens_address","req_id":"0xfc961534a0a55b925db2c5ee546c8a019c0d78d5","args":{"config_path":"ens_address","address":"0xfc961534a0a55b925db2c5ee546c8a019c0d78d5"}},{"config_path":"ens_address","req_id":"0xce92725edddb3d36e9dc8e250093f78dcd7f4012","args":{"config_path":"ens_address","address":"0xce92725edddb3d36e9dc8e250093f78dcd7f4012"}},{"config_path":"ens_address","req_id":"0x7b90bd197e7095b1e3628c435732762246a678c6","args":{"config_path":"ens_address","address":"0x7b90bd197e7095b1e3628c435732762246a678c6"}},{"config_path":"ens_address","req_id":"0x213feeba73637f958e0ec1c483138b9a37f544b9","args":{"config_path":"ens_address","address":"0x213feeba73637f958e0ec1c483138b9a37f544b9"}},{"config_path":"ens_address","req_id":"0xfafb53ffcc11d8cb6f3afbb5d4f3a3a3e1ac7c4f","args":{"config_path":"ens_address","address":"0xfafb53ffcc11d8cb6f3afbb5d4f3a3a3e1ac7c4f"}},{"config_path":"ens_address","req_id":"0x95594d85755615c515e3630512a2cd103bded787","args":{"config_path":"ens_address","address":"0x95594d85755615c515e3630512a2cd103bded787"}},{"config_path":"ens_address","req_id":"0xf6fe5b2b625a237b9fe1eef2bdbc156d4866e28d","args":{"config_path":"ens_address","address":"0xf6fe5b2b625a237b9fe1eef2bdbc156d4866e28d"}},{"config_path":"ens_address","req_id":"0x40bd1676acf10f536af1fd21df9b24915b771b63","args":{"config_path":"ens_address","address":"0x40bd1676acf10f536af1fd21df9b24915b771b63"}},{"config_path":"ens_address","req_id":"0x87d9c2d9990a9f3a18f1377ff20d9945f9eb3792","args":{"config_path":"ens_address","address":"0x87d9c2d9990a9f3a18f1377ff20d9945f9eb3792"}},{"config_path":"ens_address","req_id":"0xc43c64a1cd70b8dd14ffd7b7f53aa647b08b9a24","args":{"config_path":"ens_address","address":"0xc43c64a1cd70b8dd14ffd7b7f53aa647b08b9a24"}},{"config_path":"ens_address","req_id":"0x632ec46e174ffe3d0441e10e5b610db067b886b9","args":{"config_path":"ens_address","address":"0x632ec46e174ffe3d0441e10e5b610db067b886b9"}},{"config_path":"ens_address","req_id":"0x18f7f9d26d8367db85b5a410da9ce51e9a66badd","args":{"config_path":"ens_address","address":"0x18f7f9d26d8367db85b5a410da9ce51e9a66badd"}},{"config_path":"ens_address","req_id":"0x7d94aa1b285ecac3171b8f92bba7ad9c6ae95049","args":{"config_path":"ens_address","address":"0x7d94aa1b285ecac3171b8f92bba7ad9c6ae95049"}},{"config_path":"ens_address","req_id":"0x024a5759752d74bc3c474453811be4dded94d16a","args":{"config_path":"ens_address","address":"0x024a5759752d74bc3c474453811be4dded94d16a"}},{"config_path":"ens_address","req_id":"0xc64a854d948435c1fe97d1e4a371c698a9b79aea","args":{"config_path":"ens_address","address":"0xc64a854d948435c1fe97d1e4a371c698a9b79aea"}},{"config_path":"ens_address","req_id":"0x72b5b886e00ebb9407c7e39e1cee02bca153b1ac","args":{"config_path":"ens_address","address":"0x72b5b886e00ebb9407c7e39e1cee02bca153b1ac"}},{"config_path":"ens_address","req_id":"0xf684d0b546405eaa848e7f0cdc59f53cca47db17","args":{"config_path":"ens_address","address":"0xf684d0b546405eaa848e7f0cdc59f53cca47db17"}},{"config_path":"ens_address","req_id":"0x6d81fbdba7cc3afb7926f80c734965746b297668","args":{"config_path":"ens_address","address":"0x6d81fbdba7cc3afb7926f80c734965746b297668"}},{"config_path":"ens_address","req_id":"0x2ee42248515e55119aa0cc695b575451a77ce0f8","args":{"config_path":"ens_address","address":"0x2ee42248515e55119aa0cc695b575451a77ce0f8"}},{"config_path":"ens_address","req_id":"0xe0b17a7b6609fa841d7439ea6c5afe2fb07f8bac","args":{"config_path":"ens_address","address":"0xe0b17a7b6609fa841d7439ea6c5afe2fb07f8bac"}},{"config_path":"ens_address","req_id":"0x9333c471fb0abb0a189189933bfc0d1a4584c9f7","args":{"config_path":"ens_address","address":"0x9333c471fb0abb0a189189933bfc0d1a4584c9f7"}},{"config_path":"ens_address","req_id":"0xc8640e293667fb614596a9e404b5127e0670a3fc","args":{"config_path":"ens_address","address":"0xc8640e293667fb614596a9e404b5127e0670a3fc"}},{"config_path":"ens_address","req_id":"0x4789f8ed86858dd6879104781293a98569b46b16","args":{"config_path":"ens_address","address":"0x4789f8ed86858dd6879104781293a98569b46b16"}},{"config_path":"ens_address","req_id":"0x8999d8cb1d26c3f7388cb52de9ef4e6b1a10211f","args":{"config_path":"ens_address","address":"0x8999d8cb1d26c3f7388cb52de9ef4e6b1a10211f"}},{"config_path":"ens_address","req_id":"0x3de16382b91f59f544922bc7323fb9802b40d5c0","args":{"config_path":"ens_address","address":"0x3de16382b91f59f544922bc7323fb9802b40d5c0"}},{"config_path":"ens_address","req_id":"0x980fac1078bf614fb1d3515068a20c077b30a5bd","args":{"config_path":"ens_address","address":"0x980fac1078bf614fb1d3515068a20c077b30a5bd"}},{"config_path":"ens_address","req_id":"0x241f73a132f5dc9e0a352d360f6b9bd9bfee5dd7","args":{"config_path":"ens_address","address":"0x241f73a132f5dc9e0a352d360f6b9bd9bfee5dd7"}},{"config_path":"ens_address","req_id":"0x5389d163b11e4ae0eef597a3787c1033b80f787e","args":{"config_path":"ens_address","address":"0x5389d163b11e4ae0eef597a3787c1033b80f787e"}},{"config_path":"ens_address","req_id":"0x18d27bae9b7ff84d26ed9927fbcea320f56328b5","args":{"config_path":"ens_address","address":"0x18d27bae9b7ff84d26ed9927fbcea320f56328b5"}},{"config_path":"ens_address","req_id":"0x9ac76280cfb0e1534d08f04300bfc7b4e39608e5","args":{"config_path":"ens_address","address":"0x9ac76280cfb0e1534d08f04300bfc7b4e39608e5"}},{"config_path":"ens_address","req_id":"0x9c3bacade6bbe81a6238110a28628512abf4ec4a","args":{"config_path":"ens_address","address":"0x9c3bacade6bbe81a6238110a28628512abf4ec4a"}},{"config_path":"ens_address","req_id":"0x1221fba732e1f1e48585d7c3f4993cfc62094e6e","args":{"config_path":"ens_address","address":"0x1221fba732e1f1e48585d7c3f4993cfc62094e6e"}},{"config_path":"ens_address","req_id":"0x50d6102774fe54dd7d073a27f45dffacb51fa667","args":{"config_path":"ens_address","address":"0x50d6102774fe54dd7d073a27f45dffacb51fa667"}},{"config_path":"ens_address","req_id":"0x15c2374f1139637c377c5fea11dfcc0d5c06566a","args":{"config_path":"ens_address","address":"0x15c2374f1139637c377c5fea11dfcc0d5c06566a"}},{"config_path":"ens_address","req_id":"0x25fdda95197f804316f5ba8dbb66ac173ee19981","args":{"config_path":"ens_address","address":"0x25fdda95197f804316f5ba8dbb66ac173ee19981"}},{"config_path":"ens_address","req_id":"0x05f644c2ee80bb36921ca29c65d180017b5744ee","args":{"config_path":"ens_address","address":"0x05f644c2ee80bb36921ca29c65d180017b5744ee"}},{"config_path":"ens_address","req_id":"0xe1216f6218e415da6cf251af3d3fbd194d0d1692","args":{"config_path":"ens_address","address":"0xe1216f6218e415da6cf251af3d3fbd194d0d1692"}},{"config_path":"ens_address","req_id":"0x42e3c1b90fb712909b09593c419d245c50942a50","args":{"config_path":"ens_address","address":"0x42e3c1b90fb712909b09593c419d245c50942a50"}},{"config_path":"ens_address","req_id":"0xbf4c796931727fce4b42e8a7f1b284681a0d5a7c","args":{"config_path":"ens_address","address":"0xbf4c796931727fce4b42e8a7f1b284681a0d5a7c"}},{"config_path":"ens_address","req_id":"0x46c16bb7f499ed5848edf5c83f1457f0793cd0ab","args":{"config_path":"ens_address","address":"0x46c16bb7f499ed5848edf5c83f1457f0793cd0ab"}},{"config_path":"ens_address","req_id":"0xead5b7d86c681c036c59cd00a0390541061c69f2","args":{"config_path":"ens_address","address":"0xead5b7d86c681c036c59cd00a0390541061c69f2"}},{"config_path":"ens_address","req_id":"0x0e8b0cdf27b9dd2ddec656ed31bb086b8aed495c","args":{"config_path":"ens_address","address":"0x0e8b0cdf27b9dd2ddec656ed31bb086b8aed495c"}},{"config_path":"ens_address","req_id":"0x936a0301c3af70735cba249d5f3a96559028f880","args":{"config_path":"ens_address","address":"0x936a0301c3af70735cba249d5f3a96559028f880"}},{"config_path":"ens_address","req_id":"0x48b211039586619b04cfb3b040cdd12165e3a9cf","args":{"config_path":"ens_address","address":"0x48b211039586619b04cfb3b040cdd12165e3a9cf"}},{"config_path":"ens_address","req_id":"0x8493eca71bbe028ce959c760e209e3ad73ecc86c","args":{"config_path":"ens_address","address":"0x8493eca71bbe028ce959c760e209e3ad73ecc86c"}},{"config_path":"ens_address","req_id":"0x864de5bbaf4b8c808e94a8385b95b0855d170137","args":{"config_path":"ens_address","address":"0x864de5bbaf4b8c808e94a8385b95b0855d170137"}},{"config_path":"ens_address","req_id":"0x090f2202fc1abc9b30dc7b069629a24612f69aae","args":{"config_path":"ens_address","address":"0x090f2202fc1abc9b30dc7b069629a24612f69aae"}},{"config_path":"ens_address","req_id":"0x6ffbb6c376d0cf590289671d652ae92213614828","args":{"config_path":"ens_address","address":"0x6ffbb6c376d0cf590289671d652ae92213614828"}},{"config_path":"ens_address","req_id":"0xa3deb012dca06b12a7e9ae06738fccb4d39a6324","args":{"config_path":"ens_address","address":"0xa3deb012dca06b12a7e9ae06738fccb4d39a6324"}},{"config_path":"ens_address","req_id":"0x0c1e99991dd2f7d374bff13f9f52284ce6cfdae5","args":{"config_path":"ens_address","address":"0x0c1e99991dd2f7d374bff13f9f52284ce6cfdae5"}},{"config_path":"ens_address","req_id":"0xad997638331eab4eb8518cf299c11175696a249d","args":{"config_path":"ens_address","address":"0xad997638331eab4eb8518cf299c11175696a249d"}},{"config_path":"ens_address","req_id":"0x9e2939ef01810aec27826ba58260b7452e8ca529","args":{"config_path":"ens_address","address":"0x9e2939ef01810aec27826ba58260b7452e8ca529"}},{"config_path":"ens_address","req_id":"0x610adb9bf74987595c1e42dea73a9e7a61acb607","args":{"config_path":"ens_address","address":"0x610adb9bf74987595c1e42dea73a9e7a61acb607"}},{"config_path":"ens_address","req_id":"0xf89d67a69d5f622ee2e2b8722720d85554799051","args":{"config_path":"ens_address","address":"0xf89d67a69d5f622ee2e2b8722720d85554799051"}},{"config_path":"ens_address","req_id":"0x944847b9fb94d6fe53f99e4d0d4c75a5643597cf","args":{"config_path":"ens_address","address":"0x944847b9fb94d6fe53f99e4d0d4c75a5643597cf"}},{"config_path":"ens_address","req_id":"0xda599dedef2d8c00c01cd047bbbedc7399ad5908","args":{"config_path":"ens_address","address":"0xda599dedef2d8c00c01cd047bbbedc7399ad5908"}},{"config_path":"ens_address","req_id":"0x0046e6b678371f3576408873b3941b9ab10e3c72","args":{"config_path":"ens_address","address":"0x0046e6b678371f3576408873b3941b9ab10e3c72"}},{"config_path":"ens_address","req_id":"0x1f0f5057f7e139d8e871477563d2b96f70898d09","args":{"config_path":"ens_address","address":"0x1f0f5057f7e139d8e871477563d2b96f70898d09"}},{"config_path":"ens_address","req_id":"0x815ac0ccf85bab38b1953a008f80bb028bfc317a","args":{"config_path":"ens_address","address":"0x815ac0ccf85bab38b1953a008f80bb028bfc317a"}},{"config_path":"ens_address","req_id":"0x53a2c0823553bebbd6b89a3bcda80f3b60498fc2","args":{"config_path":"ens_address","address":"0x53a2c0823553bebbd6b89a3bcda80f3b60498fc2"}},{"config_path":"ens_address","req_id":"0x2782caccdf7f29aedc05567231d48ecd08850da6","args":{"config_path":"ens_address","address":"0x2782caccdf7f29aedc05567231d48ecd08850da6"}},{"config_path":"ens_address","req_id":"0xeefb745e597f887d6d1cf4e474134c6e71c06fb9","args":{"config_path":"ens_address","address":"0xeefb745e597f887d6d1cf4e474134c6e71c06fb9"}},{"config_path":"ens_address","req_id":"0x68fe69bfc4d7197232bca722f08baae3d51dd4d3","args":{"config_path":"ens_address","address":"0x68fe69bfc4d7197232bca722f08baae3d51dd4d3"}},{"config_path":"ens_address","req_id":"0x9033de302ee6d0ba067ea75fa2ef8b011ce13336","args":{"config_path":"ens_address","address":"0x9033de302ee6d0ba067ea75fa2ef8b011ce13336"}},{"config_path":"ens_address","req_id":"0xdc18dbdd2bb4989df627d48d4d33ecf3fb86546c","args":{"config_path":"ens_address","address":"0xdc18dbdd2bb4989df627d48d4d33ecf3fb86546c"}},{"config_path":"ens_address","req_id":"0xf5c13c0050e88a721b61c4739902dc484bf28ada","args":{"config_path":"ens_address","address":"0xf5c13c0050e88a721b61c4739902dc484bf28ada"}},{"config_path":"ens_address","req_id":"0x4f8e9db29e101ccb5505ad40bfdfca74f68a9ae9","args":{"config_path":"ens_address","address":"0x4f8e9db29e101ccb5505ad40bfdfca74f68a9ae9"}},{"config_path":"ens_address","req_id":"0x381b4b6f8a2375a8f1f6d9f55ee3a876c974ea1a","args":{"config_path":"ens_address","address":"0x381b4b6f8a2375a8f1f6d9f55ee3a876c974ea1a"}},{"config_path":"ens_address","req_id":"0x3c689fe81ab85871ab89fbeb9716f9df2f8cf5da","args":{"config_path":"ens_address","address":"0x3c689fe81ab85871ab89fbeb9716f9df2f8cf5da"}},{"config_path":"ens_address","req_id":"0x56aa44673a121c1c2f21d251f09dfb1265f0bc8d","args":{"config_path":"ens_address","address":"0x56aa44673a121c1c2f21d251f09dfb1265f0bc8d"}},{"config_path":"ens_address","req_id":"0xe940636a18e2f23f550cc3fc49b881474049cebb","args":{"config_path":"ens_address","address":"0xe940636a18e2f23f550cc3fc49b881474049cebb"}},{"config_path":"ens_address","req_id":"0x82d1883ca96e57773429e785f195e32783b1c246","args":{"config_path":"ens_address","address":"0x82d1883ca96e57773429e785f195e32783b1c246"}},{"config_path":"ens_address","req_id":"0xcbc6e296a9d52a8aa07ec524315be6e8582f3320","args":{"config_path":"ens_address","address":"0xcbc6e296a9d52a8aa07ec524315be6e8582f3320"}},{"config_path":"ens_address","req_id":"0x75b6bcf398c2c98f832aba4a7bd860d0744b5b9c","args":{"config_path":"ens_address","address":"0x75b6bcf398c2c98f832aba4a7bd860d0744b5b9c"}},{"config_path":"ens_address","req_id":"0x5eadc51e3c1d8ff43980ee6e44bafd7adb8e3c37","args":{"config_path":"ens_address","address":"0x5eadc51e3c1d8ff43980ee6e44bafd7adb8e3c37"}},{"config_path":"ens_address","req_id":"0xbdfc087a5c32f6b6e425697c1a19a10e378136ee","args":{"config_path":"ens_address","address":"0xbdfc087a5c32f6b6e425697c1a19a10e378136ee"}},{"config_path":"ens_address","req_id":"0xe341763ec08265f7040bde2236a70d9f653c6744","args":{"config_path":"ens_address","address":"0xe341763ec08265f7040bde2236a70d9f653c6744"}},{"config_path":"ens_address","req_id":"0x5497e378f7bc82892427971b52f511858717100c","args":{"config_path":"ens_address","address":"0x5497e378f7bc82892427971b52f511858717100c"}},{"config_path":"ens_address","req_id":"0x586634c272dfa3894ee9b99836541dee35660f34","args":{"config_path":"ens_address","address":"0x586634c272dfa3894ee9b99836541dee35660f34"}},{"config_path":"ens_address","req_id":"0xb1577413d0456d1a04c5d5978637759e84fda356","args":{"config_path":"ens_address","address":"0xb1577413d0456d1a04c5d5978637759e84fda356"}},{"config_path":"ens_address","req_id":"0x3bc3a083d85905afdff3e20b4802b10dbd21bd9f","args":{"config_path":"ens_address","address":"0x3bc3a083d85905afdff3e20b4802b10dbd21bd9f"}},{"config_path":"ens_address","req_id":"0x18398ef8653fe5b8acd12cc10cf645ed67258d04","args":{"config_path":"ens_address","address":"0x18398ef8653fe5b8acd12cc10cf645ed67258d04"}},{"config_path":"ens_address","req_id":"0x79d5072c72c3d610894de1274849f1b50438721c","args":{"config_path":"ens_address","address":"0x79d5072c72c3d610894de1274849f1b50438721c"}},{"config_path":"ens_address","req_id":"0x2f6939b9081d599a6c271bc6c8c0091ef7173714","args":{"config_path":"ens_address","address":"0x2f6939b9081d599a6c271bc6c8c0091ef7173714"}},{"config_path":"ens_address","req_id":"0x77e1ca9eb6746c5468cf34307618553657550dd9","args":{"config_path":"ens_address","address":"0x77e1ca9eb6746c5468cf34307618553657550dd9"}},{"config_path":"ens_address","req_id":"0x10994c5775c2a825e15bc016fb03dec068a650ac","args":{"config_path":"ens_address","address":"0x10994c5775c2a825e15bc016fb03dec068a650ac"}},{"config_path":"ens_address","req_id":"0xf622101e8f0e955ed714799ad17c21992c8f243b","args":{"config_path":"ens_address","address":"0xf622101e8f0e955ed714799ad17c21992c8f243b"}},{"config_path":"ens_address","req_id":"0xa74e65f8bee81a717de22cc49d798caa11fb494a","args":{"config_path":"ens_address","address":"0xa74e65f8bee81a717de22cc49d798caa11fb494a"}},{"config_path":"ens_address","req_id":"0x5e95b00eb048ba226e37f5fcbab2ebd8b530c83b","args":{"config_path":"ens_address","address":"0x5e95b00eb048ba226e37f5fcbab2ebd8b530c83b"}},{"config_path":"ens_address","req_id":"0xf98f3faabc33db5d781ba5a2da687a1332d1781d","args":{"config_path":"ens_address","address":"0xf98f3faabc33db5d781ba5a2da687a1332d1781d"}},{"config_path":"ens_address","req_id":"0x8a3351dfba55220076879cf03b9fa39b1120a94d","args":{"config_path":"ens_address","address":"0x8a3351dfba55220076879cf03b9fa39b1120a94d"}},{"config_path":"ens_address","req_id":"0xb219df61517a3ecbad351c9fa458e76360fe81eb","args":{"config_path":"ens_address","address":"0xb219df61517a3ecbad351c9fa458e76360fe81eb"}},{"config_path":"ens_address","req_id":"0xd8696bbd8ce60804f0fc9fdbb73b517e72855f2c","args":{"config_path":"ens_address","address":"0xd8696bbd8ce60804f0fc9fdbb73b517e72855f2c"}},{"config_path":"ens_address","req_id":"0x805131c05f6b1b768f84efbe961c89f3e3a9e990","args":{"config_path":"ens_address","address":"0x805131c05f6b1b768f84efbe961c89f3e3a9e990"}},{"config_path":"ens_address","req_id":"0x30ee1f53c0e9489fdeb7047d005684d641bafb37","args":{"config_path":"ens_address","address":"0x30ee1f53c0e9489fdeb7047d005684d641bafb37"}},{"config_path":"ens_address","req_id":"0x6cc1dce331b5be1c3fc38babd50f6f1b64fb2fe6","args":{"config_path":"ens_address","address":"0x6cc1dce331b5be1c3fc38babd50f6f1b64fb2fe6"}},{"config_path":"ens_address","req_id":"0x7e9a6b14e78bf18bd483d208af423b96ab5075a4","args":{"config_path":"ens_address","address":"0x7e9a6b14e78bf18bd483d208af423b96ab5075a4"}},{"config_path":"ens_address","req_id":"0xc8bea1ed5d2420c9bd3213a1de0e518ffbca8ea8","args":{"config_path":"ens_address","address":"0xc8bea1ed5d2420c9bd3213a1de0e518ffbca8ea8"}},{"config_path":"ens_address","req_id":"0xce797b56f9637aaf4058c38093949aafbf48ef57","args":{"config_path":"ens_address","address":"0xce797b56f9637aaf4058c38093949aafbf48ef57"}},{"config_path":"ens_address","req_id":"0xa31aeea459c1ab0124ed44711a678d6e18874692","args":{"config_path":"ens_address","address":"0xa31aeea459c1ab0124ed44711a678d6e18874692"}},{"config_path":"ens_address","req_id":"0x1a986b2d01020d4b066a7abebf6163a2b7f35004","args":{"config_path":"ens_address","address":"0x1a986b2d01020d4b066a7abebf6163a2b7f35004"}},{"config_path":"ens_address","req_id":"0x91bfef81dd0e37e879aeb4d0358c7ada6ee9106c","args":{"config_path":"ens_address","address":"0x91bfef81dd0e37e879aeb4d0358c7ada6ee9106c"}},{"config_path":"ens_address","req_id":"0x6803bc6e4bd209537eb356feb03c66ba4a383f1c","args":{"config_path":"ens_address","address":"0x6803bc6e4bd209537eb356feb03c66ba4a383f1c"}},{"config_path":"ens_address","req_id":"0x537875ef902e5c9749a8ba4c9ebf34d9734da1dc","args":{"config_path":"ens_address","address":"0x537875ef902e5c9749a8ba4c9ebf34d9734da1dc"}},{"config_path":"ens_address","req_id":"0x99e94142353411264731105fe38ff02dfe1f3c3a","args":{"config_path":"ens_address","address":"0x99e94142353411264731105fe38ff02dfe1f3c3a"}},{"config_path":"ens_address","req_id":"0x291e4ebb46c04d87c2fb10582b20e9258a1a83f8","args":{"config_path":"ens_address","address":"0x291e4ebb46c04d87c2fb10582b20e9258a1a83f8"}},{"config_path":"ens_address","req_id":"0x26ea98105ed944197f8ecae2b875a661a415e6af","args":{"config_path":"ens_address","address":"0x26ea98105ed944197f8ecae2b875a661a415e6af"}},{"config_path":"ens_address","req_id":"0x23367f74b32e7dbbc283d00d7df69b6ef323f718","args":{"config_path":"ens_address","address":"0x23367f74b32e7dbbc283d00d7df69b6ef323f718"}},{"config_path":"ens_address","req_id":"0x3dbe2b199e14e7450eea130b5f6b468c8c7dfd8b","args":{"config_path":"ens_address","address":"0x3dbe2b199e14e7450eea130b5f6b468c8c7dfd8b"}},{"config_path":"ens_address","req_id":"0x1648c13a8ed3ffb194b2c033497a5e82e543cb82","args":{"config_path":"ens_address","address":"0x1648c13a8ed3ffb194b2c033497a5e82e543cb82"}},{"config_path":"ens_address","req_id":"0x3dd1b351cb625b5edfc92c4975bed22ef028e942","args":{"config_path":"ens_address","address":"0x3dd1b351cb625b5edfc92c4975bed22ef028e942"}},{"config_path":"ens_address","req_id":"0x1e27c17432abff8e314b421be50c63a42d3e95e0","args":{"config_path":"ens_address","address":"0x1e27c17432abff8e314b421be50c63a42d3e95e0"}},{"config_path":"ens_address","req_id":"0x2f60d1bc9a80e901b9bd20b433f8a941f3b695f8","args":{"config_path":"ens_address","address":"0x2f60d1bc9a80e901b9bd20b433f8a941f3b695f8"}},{"config_path":"ens_address","req_id":"0x584918c2ed491fffbc324f9d78b31d199c9ca22d","args":{"config_path":"ens_address","address":"0x584918c2ed491fffbc324f9d78b31d199c9ca22d"}},{"config_path":"ens_address","req_id":"0xc251268d5c0506cff46e8ce609f29e4454f53892","args":{"config_path":"ens_address","address":"0xc251268d5c0506cff46e8ce609f29e4454f53892"}},{"config_path":"ens_address","req_id":"0x6cc78993fc28d60b6653a2e7e89d6a5b69975e6b","args":{"config_path":"ens_address","address":"0x6cc78993fc28d60b6653a2e7e89d6a5b69975e6b"}},{"config_path":"ens_address","req_id":"0x7425d784b866486fd8be134df053f6cc4b6a0c30","args":{"config_path":"ens_address","address":"0x7425d784b866486fd8be134df053f6cc4b6a0c30"}},{"config_path":"ens_address","req_id":"0x305ed865ea96ca9b3cf28cb9ccda2b5c6e34781e","args":{"config_path":"ens_address","address":"0x305ed865ea96ca9b3cf28cb9ccda2b5c6e34781e"}},{"config_path":"ens_address","req_id":"0xbbbc1f6be7a36f9b49f807ae24ed7ebab34d82ce","args":{"config_path":"ens_address","address":"0xbbbc1f6be7a36f9b49f807ae24ed7ebab34d82ce"}},{"config_path":"ens_address","req_id":"0x3eca5eee06a42a11ae1bf3aba57f46a2906e9154","args":{"config_path":"ens_address","address":"0x3eca5eee06a42a11ae1bf3aba57f46a2906e9154"}},{"config_path":"ens_address","req_id":"0x334201bc381d671352c4fb8d3bff998636bb06cb","args":{"config_path":"ens_address","address":"0x334201bc381d671352c4fb8d3bff998636bb06cb"}}]}
                            }                            


services_data = [
    {
        "api_service": "run_service",
        "service_name": "run",
        "configs": [
            terrible_client_request,
            {"config": "example", "arg1": "EXAMPLE", "arg2": "EXAMPLE2"},
            {
                "config": "complete_pool_stats",
                "pool_id": "0xd417ff54652c09bd9f31f216b1a2e5d1e28c1dce1ba840c40d16f2b4d09b5902",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "complete_pool_stats",
                "chain_id": "0x1",
                "base": "0x0000000000000000000000000000000000000000",
                "quote": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "pool_idx": "420",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "ens_address",
                "address": "0xE09de95d2A8A73aA4bFa6f118Cd1dcb3c64910Dc",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "price",
                "token_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "realtime_price",
                "token_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "supported_chain_ids": ["0x1"],
            },
        ],
    },
]

STAGING_BASE_URL = (
    "https://crocswap-analytics-tools-service-staging-dfxb5x3tja-uc.a.run.app"
)
PRODUCTION_BASE_URL = "https://crocswap-analytics-tools-service-dfxb5x3tja-uc.a.run.app"

def generate_tests():
    generated_tests = []
    for service_data in services_data:
        for config in service_data["configs"]:
            chain_ids = config.get("supported_chain_ids", default_chain_ids)
            for chain_id in chain_ids:
                args = config.copy()
                args.pop("supported_chain_ids", "")
                test_entry = {
                    "api_service": service_data["api_service"],
                    "service_name": service_data["service_name"],
                    "args": args,
                }

                if chain_id:
                    test_entry["args"]["chain_id"] = chain_id
                generated_tests.append(test_entry)

    return generated_tests

class Command:
    def setUp(self, config):
        self.config = config

    def tearDown(self):
        pass

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Execute method must be implemented in subclasses")


class CLICommand(Command):
    def execute(self, req):
        
        cli_command = ["python3", "run_service" + ".py"]
        for key, val in req.items():
            cli_command.append("--" + key)
            cli_command.append(val)

        call_result = subprocess.run(cli_command, capture_output=True)
        process = subprocess.Popen(cli_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()    
        
        result = {}
        result = {"call":req.copy()}
        try:
            result["data"]=json.loads(result)
            result["error"]=None
        except:
            result["data"]=str(stdout)
            result["error"]= "COULD NOT PARSE RESPONSE"
        return result


class PythonCommand(Command):
    def execute(self, req):
        cli_command = ["python3", "run_service" + ".py"]
        for key, val in req.items():
            cli_command.append("--" + key)
            cli_command.append(val)
        
        result = {}
        result = {"call":req.copy()}
        out = ""
        try:
            from run_service import run
            out = run(chain_id= "0x1", service_name= req["config"], include_data= "0", unknown_dict= req)
            result["error"]=None
            if 'error' in out:
                result["error"] = out["error"]
            result["data"]=out
        except:
            import traceback as tb
            result["data"]=out
            result["error"]= tb.format_exc()
        return result

class LocalAPICommand(Command):
    def kill_processes_by_name(self, process_name):
        try:
            subprocess.check_call(["pkill", "-f", process_name])
        except subprocess.CalledProcessError:
            pass
    
    def setUp(self,config):
        self.kill_processes_by_name("run_server.py")
        try:
            cmd = ["python3", "run_server.py"]
            self.proc =  subprocess.Popen(cmd)  
        except:
            pass
        time.sleep(7)    
    def tearDown(self):
        try:
            self.proc.terminate()
            self.proc.wait()
        except:
            pass
        self.kill_processes_by_name("run_server.py")        
        
    def execute(self, req):
        base_url = "http://localhost:8080"
        url = f"{base_url}/run"
        query_params = req.copy()
        query_params["service"] = "run"
        query_params["config_path"] = query_params.pop("config")
        query_params["include_data"] = 0
        response = requests.post(url, json=query_params)
        result = {"call":req.copy()}
        try:
            result["data"] = response.json()
            result["error"] = None
            assert not "error" in result["data"]
        except json.JSONDecodeError:
            result["data"] = response.text
            result["error"] = "Failed to parse JSON"

        return result

class LocalRunningAPICommand(Command):
    def setUp(self,config):
        pass
           
    def tearDown(self):
        pass 
        
    def execute(self, req):
        base_url = "http://localhost:8080"
        url = f"{base_url}/run"
        query_params = req.copy()
        query_params["service"] = "run"
        query_params["config_path"] = query_params.pop("config")
        query_params["include_data"] = 0
        response = requests.post(url, json=query_params)
        result = {"call":req.copy()}
        try:
            result["data"] = response.json()
            result["error"] = None
            assert not "error" in result["data"]
        except json.JSONDecodeError:
            result["data"] = response.text
            result["error"] = "Failed to parse JSON"

        return result

class StageAPICommand(Command):

    def setUp(self,config):
        pass
    def tearDown(self):
        pass
        
    def execute(self, req):
        base_url = "https://crocswap-analytics-tools-service-staging-dfxb5x3tja-uc.a.run.app"
        url = f"{base_url}/run"
        query_params = req.copy()
        query_params["service"] = "run"
        query_params["config_path"] = query_params.pop("config")
        query_params["include_data"] = 0
        response = requests.post(url, json=query_params)
        result = {"call":req.copy()}
        try:
            result["data"] = response.json()
            result["error"] = None
            assert not "error" in result["data"]
        except json.JSONDecodeError:
            result["data"] = response.text
            result["error"] = "Failed to parse JSON"

        return result

import gevent
global TheCommand

class BasicTest(unittest.TestCase):
    def setUp(self):
        print("RUNNING BASIC TEST SETUP")
        self.command = TheCommand()
        self.command.setUp(config={})
    def tearDown(self):
        self.command.tearDown()

    def do_run(self):
        tests = generate_tests()
        results = []
        try:
            self.command 
        except:
            self.command = TheCommand()
        for service_call in tests:
            try:
                res = self.command.execute(service_call["args"])
                assert 'data' in res
                assert 'error' in res                
            except:
                import traceback as tb
                res = {"call":service_call,"data":None,"error":tb.format_exc()}
            results.append(res)        
        return results        
        
    def test_run(self):
        results = self.do_run()
        for result in results:
            if result['error'] != None:
                print("found an invalid response")
                pprint.pprint(str(result)[0:10])
            assert result['error'] == None
    

class BasicLocustUser(HttpUser):
    wait_time = between(0,1)

    def on_start(self):
        self.test = BasicTest()

    def on_stop(self):
        pass

    @task
    def run_basic_test(self):
        try:
            results = self.test.do_run() 
            for r in results:
                error = None
                if 'error' in r and r['error']:
                    error = r['error']
                events.request.fire(request_type="test",
                                    name="BasicTest",
                                    response_time=0,
                                    response_length=0,
                                       exception=error,results=results)                
        except Exception as e:
            import traceback as tb
            events.request.fire(request_type="test",
                    name="BasicTest",
                    response_time=0,
                    response_length=0,
                       exception=tb.format_exc(),results=None)   


class LoadTest(unittest.TestCase):
    def setUp(self):
        self.env = Environment(user_classes=[BasicLocustUser], host="http://localhost:8080")
        self.env.create_local_runner()        
        self.command = TheCommand()
        self.command.setUp({})
        self.runs = 0;
        self.fails = 0;
        self.successes = [];
        self.messages = [];
        self.ambiguous_messages = [];
        
        @events.request.add_listener
        def on_request(request_type, name, response_time, response_length,exception, **kwargs):
            if (exception):
                self.ambiguous_messages.append(kwargs['results'])                    
                if not "ngreenlet.GreenletExit" in str (kwargs['results']) and len (str(exception)) > 0:
                    self.fails = self.fails +1
                    try:
                        self.messages.append(json.loads(kwargs['results']))
                    except:
                        self.messages.append(kwargs['results'])
                    #print(kwargs['results']['data'])
            self.runs += 1
            self.runs = self.runs +1
        
    def tearDown(self):
        self.command.tearDown()

    def test_load(self):
        self.env.runner.start(user_count=10, spawn_rate=2)
        def finish():
            pass
        gevent.spawn_later(10, finish)
        self.env.runner.greenlet.join(timeout=120)
        print ("Testing results")
        print ("runs",  self.runs)
        print ("fails",  self.fails)
        with open("failures.txt","w") as f:
            try:
                f.write(json.dumps(self.messages[0:10]))
            except:
                f.write(str(self.messages[0:10]))
        
        with open("potential_failures.txt","w") as f:
            try:
                f.write(json.dumps(self.ambiguous_messages))
            except:
                f.write(str(self.ambiguous_messages))
                      

def main(command, test_case):
    global TheCommand
    commands = {
        'CLICommand':CLICommand,
        'StageAPI': StageAPICommand,
        'LocalAPI': LocalAPICommand,
        'LocalRunningAPICommand':LocalRunningAPICommand,
        'Python': PythonCommand
    }
    test_case = {
        'BasicTest': BasicTest,
        'LoadTest': LoadTest
    }.get(args.test, BasicTest) 
    TheCommand = commands.get(command, PythonCommand)

    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a specified test case with a specific command')
    parser.add_argument('--command', help='The command to use (StageAPI, LocalAPI, ,CLICommand, Python)', default='Python')
    parser.add_argument('--test', help='The test case to run (LoadTest [Will cause failures and crashes!], BasicTest)', default='BasicTest')

    args = parser.parse_args()
    main(args.command, args.test)

# python3 run_test.py --command LocalAPI --test BasicTest
# python3 run_test.py --command LocalRunningAPICommand --test BasicTest 
# - validate tests (pass)
# - Send repo & branch to Ben
# ---- By creating a PR in the analytics-server repo
# - Run Docker
# - Updating Docs
# - --- Env vars
# - --- Arbiturm remove constant
# - POLISH