.PHONY: all test
curdir := $(shell pwd)


build: 
	# gather all deps for python 3.6.3
	mkdir -p $(curdir)/.pipcache/3.6.3/pip
	docker build -f docker_files/tarkin_3.6.3_cache.dockerfile . -t tarkin_3.6.3_cache
	docker run -it -v $(curdir)/.pipcache/3.6.3:/root/3.6.3 tarkin_3.6.3_cache:latest cp -r /root/.cache/pip /root/3.6.3/
	
	# gather all deps for python 3.5
	mkdir -p $(curdir)/.pipcache/3.5/pip
	docker build -f docker_files/tarkin_3.5_cache.dockerfile . -t tarkin_3.5_cache
	docker run -it -v $(curdir)/.pipcache/3.5:/root/3.5 tarkin_3.5_cache:latest cp -r /root/.cache/pip /root/3.5/

	# runner for pro in python 3.6.3
	docker build -f docker_files/tarkin_pro_3.6.3.dockerfile . -t tarkin_pro_3.6.3
	# runner for test in python 3.6.3
	docker build -f docker_files/tarkin_test_3.6.3.dockerfile . -t tarkin_test_3.6.3
	# runner for pro in python 3.5
	docker build -f docker_files/tarkin_pro_3.5.dockerfile . -t tarkin_pro_3.5
	# runner for test in python 3.5
	docker build -f docker_files/tarkin_test_3.5.dockerfile . -t tarkin_test_3.5


test: 
	docker run -it tarkin_test_3.6.3:latest test.sh
	docker run -it tarkin_test_3.5:latest test.sh
