FROM selenium/standalone-chrome

WORKDIR /usr/app
#helo
# Install some depenendencies
RUN sudo apt-get update
RUN pwd
RUN sudo curl -o allure-2.13.7.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.7/allure-commandline-2.13.7.tgz
RUN sudo tar -zxvf allure-2.13.7.tgz -C /opt/
RUN sudo ln -s /opt/allure-2.13.7/bin/allure /usr/bin/allure

RUN sudo apt update
RUN sudo apt install -y software-properties-common
RUN sudo add-apt-repository -y ppa:deadsnakes/ppa
RUN sudo apt install -y python3.9
RUN sudo apt-get install -y python3-pip
RUN sudo python3.9 -m pip install --upgrade pip
RUN sudo apt-get install -y python3.9-dev
RUN sudo apt-get install -y unixodbc-dev
COPY ./docker-requirements.txt ./
RUN sudo python3.9 -m pip install -r docker-requirements.txt
COPY ./ ./
RUN sudo python3.9 -m pip install ./utilities/PyAuto-docker-2.0.0-py3-none-any.whl
RUN export PATH=/usr/app/:$PATH

WORKDIR /usr/app/tests/test_scripts/

# Default command
ENTRYPOINT ["sudo", "python3.9", "RunTest.py", "--docker"]
CMD ["--tags", "se_input_form"]

#docker build -t framework/pyauto .
#docker run -it -v %cd%/reports/report_dates/:/usr/app/reports/report_dates/ framework/pyauto --tags se_input_form
