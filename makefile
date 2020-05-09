include .env
GREEN=\n\033[1;32;40m
RED=\n\033[1;31;40m
NC=\033[0m # No Color

# WARNING: git에서 commit_hash를 가져올 때 white space가 있다.
TAG:=${CI_COMMIT_SHA} # ex) git의 tag를 사용하는 경우 v1.0.0
RELEASE:=${CI_COMMIT_SHA} # 또는 ${TAG} release format을 원하면 바꿀 수 있다


PYCODESTYLE = pycodestyle
MYPY = mypy
# no-member: mypy가 찾아줌
PYLINTFLAGS = --verbose --reports=no --output-format=colorized --errors-only --disable=no-member --enable=unused-import

PYTHONFILES := $(shell find . -name '*.py' | grep -v .venv)
PYTHON_VERSION = py38
PYTHON_LINE_LENGTH = 80
targets:
	@echo $(PYTHONFILES)
.PHONY: targets

PIP := $(shell command -v pip 2> /dev/null)
PIPENV := $(shell command -v pipenv 2> /dev/null)

ref:
ifndef PIP
	# https://pip.pypa.io/en/stable/installing/
	$(error "pip이 설치되어 있지 않습니다.")
endif
	@/bin/sh -c "echo \"${GREEN}pip 설치되어 있음${NC}\""

ifndef PIPENV
	pip install pipenv
endif
	@/bin/sh -c "echo \"${GREEN}pipenv 설치되어 있음${NC}\""

.PHONY: ref

# 의존성 모듈 관리
venv_dir=.venv
venv-dev: 
ifneq "$(wildcard $(venv_dir) )" ""
	@/bin/sh -c "echo \"${GREEN}Already installation${NC}\""
else
	@/bin/sh -c "echo \"${GREEN}pipenv install${NC}\""
	export PIPENV_VENV_IN_PROJECT=${PWD} && pipenv install --dev
	pipenv graph
endif
.PHONY: venv-dev

pycodestyle: ref venv-dev
	@/bin/sh -c "echo \"${GREEN}[pycodestyle 시작]${NC}\""
	pipenv run $(PYCODESTYLE) --first $(PYTHONFILES)
.PHONY: pycodestyle

# vscode의 formatting 도구로 black을 사용
black: ref venv-dev
	@/bin/sh -c "echo \"${GREEN}[black 시작]${NC}\""
	pipenv run black -t $(PYTHON_VERSION) -l $(PYTHON_LINE_LENGTH) $(PYTHONFILES)
.PHONY: black

pylint: ref venv-dev
	@/bin/sh -c "echo \"${GREEN}[pylint 시작]${NC}\""
	pipenv run pylint $(PYLINTFLAGS) $(PYTHONFILES)
.PHONY: fast-pylint

mypy: ref venv-dev
	@/bin/sh -c "echo \"${GREEN}[정적분석 시작]${NC}\""
	pipenv run $(MYPY) --config-file mypy.ini $(PYTHONFILES)
.PHONY: mypy

lint: pycodestyle mypy pylint
.PHONY: lint

test: ref venv-dev
	pipenv run pytest \
	--pdb \
	--cov=src tests \
	--cov-report=html \
	--cov-report=term \
	--cov-report=xml \
	--disable-warnings
.PHONY: test-coverage

build-docker: ref venv-dev requirements
	@/bin/sh -c "echo \"${GREEN}[docker image 빌드를 시작합니다]${NC}\""
	@docker build --rm -f "base.Dockerfile" -t ${APP_NAME}-base:latest "."
	@set -ex && docker build --build-arg APP_NAME=${APP_NAME}-base:latest --rm -f "app.Dockerfile" -t ${APP_NAME}:latest "."
.PHONY: build-docker

requirements: ref venv-dev
	@/bin/sh -c "echo \"${GREEN}[requirements.txt를 추출합니다]${NC}\""
	@pipenv lock -r > requirements.txt
.PHONY: requirements

# yaml에서 colon 버그 존재 이외에도 특문 버그도 존재하므로 script로 처리
# https://gitlab.com/gitlab-org/gitlab-foss/-/issues/30097
__ci_commit:
	@git add app/__init__.py
	@git commit -m "chore(version): changed version ${AGENT_VERSION}"
.PHONY: __ci_commit

# 마지막 tag로부터 현재까지의 changelog 및 버전 확인 용
current_changelog:
	@/bin/sh -c "echo \"${GREEN}[release version] $(shell yarn run standard-version --dry-run | grep tagging | cut -d ' ' -f4)${NC}\""
	@/bin/sh -c "echo \"${GREEN}[description] ${NC}\""
	@yarn run standard-version --dry-run --silent | grep -v yarn | grep -v Done | grep -v "\-\-\-" | grep -v standard-version
.PHONY: current_changelog
