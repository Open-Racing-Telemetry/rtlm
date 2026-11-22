if(CONFIG_BUILD_TRANSCEIVER)
    set(ENTRY_FILE "main_tx.cpp")
else()
    set(ENTRY_FILE "main_rx.cpp")
endif()

idf_component_register(SRCS "${ENTRY_FILE}")
