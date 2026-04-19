window.inactivityHelper = {
    register: function (dotnetHelper) {

        function resetTimer() {
            dotnetHelper.invokeMethodAsync('OnUserActivity');
        }

        window.addEventListener('mousemove', resetTimer);
        window.addEventListener('keydown', resetTimer);
        window.addEventListener('click', resetTimer);
        window.addEventListener('touchstart', resetTimer);
    },

    unregister: function () {
        window.removeEventListener('mousemove', resetTimer);
        window.removeEventListener('keydown', resetTimer);
        window.removeEventListener('click', resetTimer);
        window.removeEventListener('touchstart', resetTimer);
    }
};