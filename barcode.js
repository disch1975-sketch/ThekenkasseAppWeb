window.barcodeScanner = (function () {

    let buffer = "";
    let dotNetRef = null;

    function init(dotNetObject) {
        dotNetRef = dotNetObject;

        document.addEventListener("keydown", handleKeyDown);
    }

    function handleKeyDown(e) {

        // Enter = Scan abschließen
        if (e.key === "Enter") {

            if (buffer.length > 0 && dotNetRef) {
                dotNetRef.invokeMethodAsync("HandleScanGlobal", buffer);
            }

            buffer = "";
            return;
        }

        // nur echte Zeichen sammeln
        if (e.key.length === 1) {
            buffer += e.key;
        }

        // optional: Reset bei Escape
        if (e.key === "Escape") {
            buffer = "";
        }
    }

    function dispose() {
        document.removeEventListener("keydown", handleKeyDown);
        buffer = "";
        dotNetRef = null;
    }

    return {
        init,
        dispose
    };

})();