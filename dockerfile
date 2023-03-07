FROM ros:noetic-ros-core-focal

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python3-pip

# install ros packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-noetic-ros-base=1.5.0-1* \
    ros-noetic-rviz \
    ros-noetic-moveit \
    && rm -rf /var/lib/apt/lists/*

ENV HOME /root
WORKDIR $HOME/workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    git tmux vim \
    && rm -rf /var/lib/apt/lists/*

RUN echo "set -g mouse" > /root/.tmux.conf
RUN echo "source /opt/ros/noetic/setup.bash" > /root/.bashrc && echo "source /root/workspace/devel/setup.bash"  > /root/.bashrc

RUN apt-get update && apt-get install -y python-is-python3

RUN pip install ipython
