# Dependencies for Ubuntu 18.04 LTS

This setup is only tested on Ubuntu 18.04 LTS. Do not run Pupil on a VM unless you know what you are doing. For setting up your dependencies on Ubuntu 17.10 or lower, take a loot at [the corresponding setup guide](./dependencies-ubuntu17.md).

Most of this works via **apt**! Just copy paste into the terminal and listen to your machine purr.

## General Dependencies

```sh
sudo apt install -y pkg-config git cmake build-essential nasm wget python3-setuptools libusb-1.0-0-dev  python3-dev python3-pip python3-numpy python3-scipy libglew-dev libglfw3-dev libtbb-dev

# ffmpeg >= 3.2
sudo apt install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev ffmpeg x264 x265 libportaudio2 portaudio19-dev

# OpenCV >= 3
sudo apt install -y python3-opencv libopencv-dev

# 3D Eye model dependencies
sudo apt install -y libgoogle-glog-dev libatlas-base-dev libeigen3-dev
sudo apt install -y libceres-dev
```

## Turbojpeg

```sh
wget -O libjpeg-turbo.tar.gz https://sourceforge.net/projects/libjpeg-turbo/files/1.5.1/libjpeg-turbo-1.5.1.tar.gz/download
tar xvzf libjpeg-turbo.tar.gz
cd libjpeg-turbo-1.5.1
./configure --enable-static=no --prefix=/usr/local
sudo make install
sudo ldconfig
```

## libuvc
```sh
git clone https://github.com/pupil-labs/libuvc
cd libuvc
mkdir build
cd build
cmake ..
make && sudo make install
```

If you want to run libuvc as normal user, add the following udev rules:
```sh
echo 'SUBSYSTEM=="usb",  ENV{DEVTYPE}=="usb_device", GROUP="plugdev", MODE="0664"' | sudo tee /etc/udev/rules.d/10-libuvc.rules > /dev/null
sudo udevadm trigger
```

### Install Python Libraries

We recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for running Pupil.

```sh
# Upgrade pip to latest version. This is necessary for some dependencies.
python -m pip install --upgrade pip

pip install cysignals
pip install cython
pip install msgpack==0.5.6
pip install numexpr
pip install packaging
pip install psutil
pip install pyaudio
pip install pyopengl
pip install pyzmq
pip install scipy
pip install git+https://github.com/zeromq/pyre

pip install pupil-apriltags
pip install pupil-detectors
pip install git+https://github.com/pupil-labs/PyAV
pip install git+https://github.com/pupil-labs/pyuvc
pip install git+https://github.com/pupil-labs/pyndsi
pip install git+https://github.com/pupil-labs/pyglui
```

### OpenCV Troubleshooting
`ImportError: No module named 'cv2'`
  
When you see this error, Python cannot find the bindings from your OpenCV installation.

**We do NOT (!) recommend to install `opencv-python` via pip in that case!** 

Installing `opencv-python` will install another full (potentially different) version of opencv to your machine, so we are not recommending this setup.
When you install opencv with `sudo apt install -y python3-opencv libopencv-dev` as we advise above, you should have the `cv2` package available for import in Python as this will install compatible Python bindings already.

However, you might run into these problems when using a virtual environment, as your virtual environment cannot by default access Python packages that were installed from `apt`.
In that case there are 2 options:

1. Symlink or copy the Python bindings into your virtualenv. See e.g. [step 4 of this stackoverflow post](https://stackoverflow.com/a/37190408) for reference.
2. Create your virtualenv with the [`--system-site-packages`](https://virtualenv.pypa.io/en/latest/userguide/#the-system-site-packages-option) option, which will enable access to system-installed Python packages.

## Next Steps

That's it! You're done installing dependencies!

Now, you should be able to run Pupil from source. Follow the remaining instructions in the [README](../README.md).
