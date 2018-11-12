
(function ($) { 
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);

function loginClick(){
    location.href = "../html/dashboard.html";
    console.log("Inside login function");
    alert('alert');
}


function searchClick(){

    var departure =  document.getElementById("departure").value;
    var destination = document.getElementById("destination").value;
    var date = document.getElementById("date").value;
    console.log(departure,destination,date);

    if(departure.length ==0){
        alert('Enter departure');
        return;
    }

    if(destination.length ==0){
        alert('Enter departure');
        return;
    }

    if(date.length ==0){
        alert('Enter departure');
        return;
    }

    //var json_obj = JSON.parse(Get("https://localhost:5000/dbhandling/displayflights"))

    var tbdy = this.document.getElementById("tablebody") ;



    tbdy.innerHTML = `<tr>
                <td>321</td>
                <td>Kingfisher Airlines</td>
                
                <td>3:00</td>
                <td>30</td>
                <td>$36,738</td>
            </tr>
            <tr>
                <td>426</td>
                <td>Air India</td>
                
                <td>4:15</td>
                <td>78</td>
                <td>$23,789</td>
            </tr>
            <tr>
                <td>901</td>
                <td>Spice Jet</td>
                
                <td>11:30</td>
                <td>23</td>
                <td>$56,142</td>
            </tr>
            <tr>
                <td>234</td>
                <td>Jet Airways</td>
                
                <td>15:30</td>
                <td>200</td>
                <td>$38,735</td>
            </tr>
            <tr>
                <td>786</td>
                <td>Vistara</td>
                
                <td>21:30</td>
                <td>67</td>
                <td>$63,542</td>
            </tr>
            
             `;




    

}

function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}

function goClick(){
    alert('go clicked')

    var flight_id = document.getElementById("flightid").value;
    var classBook = document.getElementById("classbooking").value;
    var numTicket = document.getElementById("numberticket").value;

    console.log(flight_id,classBook,numTicket)

    var cost = this.document.getElementById("price");

    cost.innerHTML = 'Total cost(INR): 4000'

}

function confirmClick(){

}