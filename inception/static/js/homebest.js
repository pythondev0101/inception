window.addEventListener('load', function () {

})

function close_toast(){
    Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
    }
    NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = this.length - 1; i >= 0; i--) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}
    document.getElementById("toast-container").remove();
}

