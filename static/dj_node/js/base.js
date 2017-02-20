(
    function() {
        /*
         * nav submenu
         */
        var navMenuObj = {
            init: function(el, cls) {
                window.addEventListener("click", function(e) {
                    // remove all .clicked class
                    var elementList = document.getElementsByClassName('open-submenu');
                    for (var i = 0, length = elementList.length; i < length; i++) {
                        var element = elementList[i];
                        element.parentNode.classList.remove("clicked");
                    }

                    // add .clicked class to target
                    var targetElement = e.target;
                    if (targetElement.classList.contains('open-submenu')) {
                        targetElement.parentNode.classList.add('clicked');
                    }
                });
            }
        }
        navMenuObj.init()


        /*
         * modal
         */
        var myModalObj = {
            findAncestor: function(el, cls) {
                while ((el = el.parentElement) && !el.classList.contains(cls));
                return el;
            },
            showModal: function(btn) {
                var modal_id = btn.getAttribute('data-modal');
                var modal = document.getElementById(modal_id);
                modal.style.display = "block";
            },
            closeModal: function(btn) {
                var modal = this.findAncestor(btn, 'modal');
                modal.style.display = "none";
            },
            init: function() {
                var modalBtns = document.getElementsByClassName('modal-btn');
                for (var i = 0; i < modalBtns.length; i++) {
                    var btn_modal = modalBtns[i];
                    modalBtns[i].onclick = function(btn) {
                        return function() {
                            myModalObj.showModal(btn);
                        }
                    }(btn_modal)
                }

                var closeBtns = document.getElementsByClassName('modal-close');
                for (var i = 0; i < closeBtns.length; i++) {
                    var btn_close = closeBtns[i];
                    btn_close.onclick = function(btn) {
                        return function() {
                            myModalObj.closeModal(btn);
                        }
                    }(btn_close)
                }

                window.onclick = function(event) {
                    var modals = document.getElementsByClassName('modal');
                    var hideAll = false;
                    for (var i = 0; i < modals.length; i++) {
                        if (event.target == modals[i]) {
                            hideAll = true;
                        }
                    }

                    if (hideAll) {
                        for (var i = 0; i < modals.length; i++) {
                            modals[i].style.display = "none";
                        }
                    }
                }
            }
        }
        myModalObj.init()

        /*
         * div equal height
         */
        var eleEqHeight = {
            init: function() {
                var divs = document.getElementsByClassName('direct-child-equal');
                for (var i = 0; i < divs.length; i++) {
                    var children = divs[i].childNodes

                    //find max height
                    var maxHeight = 0;
                    for (var j = 0; j < children.length; j++) {
                        if (children[j].offsetHeight > maxHeight) {
                            maxHeight = children[j].offsetHeight;
                        }
                    }

                    //ast max height
                    for (var j = 0; j < children.length; j++) {
                        if (children[j] && children[j].className) {
                            children[j].setAttribute("style", "height:" + maxHeight + "px");
                        }
                    }
                }
            }
        }
        eleEqHeight.init()


        /*
         * city search
         */
        var citySuggest = {
            init: function() {
                var cityElements = document.getElementsByClassName('city-suggest');
                for(var i=0; i < cityElements.length; i++){
                    var cityInput = cityElements[i];
                    var awesomplete = new Awesomplete(cityInput, {
                        minChars: 1,
                        autoFirst: true
                    });
                    $(cityInput).on("keyup", function() {
                        $.ajax({
                            url: 'http://gd.geobytes.com/AutoCompleteCity?callback=?&q=' + this.value,
                            type: 'GET',
                            dataType: 'json',
                            success: function(data) {
                                var list = [];
                                $.each(data, function(key, value) {
                                    value = value.replace(", United States", "");
                                    list.push(value);
                                });
                                awesomplete.list = list;
                            }
                        })
                    });
                } //close for loop
            } //close of init()
        }
        citySuggest.init()
    }
)()


/*
 * rating
 */
var ratingObj = {
    getSiblings: function(element,  type){
        var arraySib = [];
        if ( type == 'prev' ){
            while ( element = element.previousElementSibling ){
                arraySib.push(element);
            }
        } else if ( type == 'next' ) {
            while ( element = element.nextElementSibling ){
                arraySib.push(element);
            }
        }
        return arraySib;
    },
    init: function() {
        var ratings = document.getElementsByClassName('star-rating');
        for (var i = 0; i < ratings.length; i++) {
            var starList = ratings[i].childNodes;
            for (var j = 0; j < starList.length; j++) {
                var star = starList[j];
                star.onclick = function(myStar) {
                    return function() {
                        myStar.className = "on";
                        var hiddenRating = myStar.parentElement.getElementsByClassName('rating')[0];

                        //turn on prev star
                        var previousSiblings = ratingObj.getSiblings(myStar, 'prev');
                        for (var n = 0; n < previousSiblings.length; n++) {
                            previousSiblings[n].className = "on";
                        }

                        //turn off post star
                        var nextSiblings = ratingObj.getSiblings(myStar, 'next');
                        for (var n = 0; n < nextSiblings.length; n++) {
                            nextSiblings[n].className = "off";
                        }

                        //set the input value
                        var ratingInput = myStar.parentElement.nextElementSibling;
                        ratingInput.value = 5 - nextSiblings.length;

                    }
                }(star)
            }
        }
    } //close of init()
}
ratingObj.init()