

(function() {
    // script responsible for navigation dropdown and tree actions
    var toggler = document.getElementsByClassName("caret");
    var i;
    for (i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function() {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("caret-down");
        }); 
    } 

    // script responsible for subscription timer
    for(i=0;i<subscriptions.length;i++){
        
        var subscription = subscriptions[i].fields;
        var subscription_date = moment(subscription.subscription_date,"YYYY-MM-DD");
        var expiration_date = moment(subscription.subscription_expiration_date,"YYYY-MM-DD");

        var duration = countdown(
                        subscription_date.toDate(),
                        expiration_date.toDate(),
                        countdown.DAYS|countdown.MONTHS|countdown.YEARS
                        );
        var remaining = countdown(
                        moment().toDate(),
                        expiration_date.toDate(),
                        countdown.DAYS|countdown.MONTHS|countdown.YEARS
                        );

        var dom_started = document.getElementById("started-"+subscriptions[i].pk);
        var dom_validity = document.getElementById("validity-"+subscriptions[i].pk);
        var dom_duration = document.getElementById("duration-"+subscriptions[i].pk);
        var dom_remaining = document.getElementById("remaining-"+subscriptions[i].pk);

        if(subscription_date<=expiration_date){
            document.getElementById("sub-"+subscriptions[i].pk+"-active").classList.remove("d-none");;
        }else{
            document.getElementById("sub-"+subscriptions[i].pk+"-expired").classList.remove("d-none");
        }

        dom_started.innerHTML = subscription_date.format("ddd, Do of MMMM, YYYY");
        dom_validity.innerHTML = expiration_date.format("ddd, Do of MMMM, YYYY");
        dom_duration.innerHTML = duration;
        dom_remaining.innerHTML = remaining;
    }
})();

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    document.getElementById("brand-logo").style.width = "15%";
    document.getElementById("base-breadcrumb").style.paddingTop = "2px";
    document.getElementById("base-breadcrumb").style.paddingBottom = "2px";
    document.getElementById("base-navbar-main").style.paddingTop = "1px";
    document.getElementById("base-navbar-main").style.paddingBottom = "1px";
  } else {
    document.getElementById("brand-logo").style.width = "25%";
    document.getElementById("base-breadcrumb").style.paddingTop = "12px";
    document.getElementById("base-breadcrumb").style.paddingBottom = "12px";
    document.getElementById("base-navbar-main").style.paddingTop = "8px";
    document.getElementById("base-navbar-main").style.paddingBottom = "8px";
  }
} 

//jq
$(document).ready(function(){
    $(function () {
        $('[data-toggle="popover"]').popover()
    })
});