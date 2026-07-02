MPY_CROSS = /tmp/mpy_venv/bin/mpy-cross
BUILD_DIR = build
SRC = main.py
TARGET = $(BUILD_DIR)/main.mpy

.PHONY: all build deploy clean

all: build

build: $(TARGET)

$(TARGET): $(SRC)
	mkdir -p $(BUILD_DIR)
	$(MPY_CROSS) -o $@ $(SRC)
	@echo "Built: $(SRC) -> $(TARGET)"

deploy: build
	@echo "Deploying to Pico..."
	rshell cp $(TARGET) /pyboard/main.mpy
	rshell cp $(SRC) /pyboard/main.py
	rshell repl ~ $$'\x04'
	@echo "Deployed and restarted."

clean:
	rm -rf $(BUILD_DIR)
	@echo "Cleaned."