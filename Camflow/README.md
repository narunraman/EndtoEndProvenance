# End2End Functionality

This repo serves as a way to see functionality of End to End provenance, using the tools installed via the instructions above.

## CamFlow 

##### Must have camflow-dev installed or use pre-built VM [(ova file)](https://www.dropbox.com/s/a918m7lthirnghn/Fedora_end2end.ova?dl=0)
```
git clone https://github.com/camflow/camflow-dev
cd camflow-dev
git checkout layer
make prepare
cd build/libprovenance
git checkout layer
cd ../..
make config
make compile
make install
sudo reboot now
```

### To view End to End functionality
To generate the shared object file: ```make disclose ```

To run: ```python disclose_prov.py <path-to-json>```

To view (via [camtool](https://github.com/CamFlow/camtool/)):

* go to [camflow graph viewer](http://camflow.org/demo) and click Start CamFlow MQTT
* then ```$ camtool --publish /tmp/audit.log```
