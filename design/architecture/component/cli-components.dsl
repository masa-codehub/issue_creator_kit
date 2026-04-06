# CLI Container Components
extend cli {
    main = component "CLI/Runner" "Entry point and command definitions." "cli.py, __main__.py" {
        tags "Layer:Interface" "Type:Component"
    }
}
