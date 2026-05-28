window.registerAfterPrint = function (dotnetHelper) {
    window.onafterprint = function () {
        dotnetHelper.invokeMethodAsync("OnAfterPrint");
    };
};