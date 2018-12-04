
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

    var email = document.getElementById("loginfield").value;
    var password = document.getElementById("passwordfield").value;

    console.log(email,password);

    if(email == ""){
        alert('Fill email!')
        return;
    }

    if(password == ""){
        alert('Fill password!')
        return;
    }


    // if(email == "suhas.2ab@gmail.com" && password == "password"){
    //     $.post("/postusername",{
    //         username : '\"Suhas HE\"',
    //         'password' : password
    //     });
    //     window.location.href = "/login";   
    // }
    // else if(email == "kurt@gmail.com" && password == "kenya"){
    //     location.href = "/login";
    // }
    // else{
    //     alert('Incorrect username or password')
    // }

    
    // console.log("Inside login function");

    $.post("/loginClick",
    {
        'email':email,
        'password':password
    },
    function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
        if(data == "success"){
            window.location = "/dashboard.html"
        }
        else{
            alert('Incorrect username or password')
        }
    });

}


function searchClick(){

    var dateReg = /^\d{2}[./-]\d{2}[./-]\d{4}$/ ;

    var departure =  document.getElementById("departure").value;
    var destination = document.getElementById("destination").value;
    var date = document.getElementById("date").value;
    console.log(departure,destination,date);
    var condition = false;

 

    if(departure.length ==0){
        alert('Enter departure');
        return;
    }

    if(destination.length ==0){
        alert('Enter destination');
        return;
    }

    if(date.length ==0){
        alert('Enter date');
        return;
    }

    if(date.match(dateReg)){

    }
    else{
        alert('Incorrect date format . Re Enter date!')
        return;
    }

    //var json_obj = JSON.parse(Get("https://localhost:5000/dbhandling/displayflights"))

    var tbdy = this.document.getElementById("tablebody") ;
    tbdy.innerHTML="";




    // if(condition){
    //     tbdy.innerHTML = `  
    //         <tr onclick = "window.location ='/bookflight?flightid=321' ">
    //             <td>321</td>
    //             <td>Kingfisher Airlines</td>
                
    //             <td>3:00</td>
    //             <td>30</td>
    //             <td>Rs 3,673</td>
    //             <td>Rs 4,673</td>
    //         </tr>
           
            
    //         <tr onclick = "window.location ='/bookflight?flightid=426' ">
    //             <td>426</td>
    //             <td>Air India</td>
                
    //             <td>4:15</td>
    //             <td>78</td>
    //             <td>Rs 5,021</td>
    //             <td>Rs 6,021</td>
    //         </tr>
           
    //         <tr onclick = "window.location ='/bookflight?flightid=901' ">
            
    //             <td>901</td>
    //             <td>Spice Jet</td>
                
    //             <td>11:30</td>
    //             <td>23</td>
    //             <td>Rs 4,599</td>
    //             <td>Rs 6,599</td>
    //         </tr>
           
    //         <tr onclick = "window.location ='/bookflight?flightid=234' ">
    //             <td>234</td>
    //             <td>Jet Airways</td>
                
    //             <td>15:30</td>
    //             <td>200</td>
    //             <td>Rs 3,399</td>
    //             <td>Rs 4,399</td>
    //         </tr>
           
    //         <tr onclick = "window.location ='/bookflight?flightid=786' ">
    //             <td>786</td>
    //             <td>Vistara</td>
                
    //             <td>21:30</td>
    //             <td>67</td>
    //             <td>Rs 4,599</td>
    //             <td>Rs 5,599</td>
    //         </tr>
           
    //          `;

    // }



    

}

function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}


function goClick(){
   

    var flight_id = document.getElementById("flightid").value;
    var classBook = document.getElementById("classbooking").value;
    var numTicket = document.getElementById("numberticket").value;

    console.log(flight_id,classBook,numTicket)

    if(flight_id.length == 0){
        alert('Enter flight ID');
        return
    }

    if(classBook.length == 0){
        alert('Enter booking class');
        return
    }

    if(numTicket.length == 0){
        alert('Enter numTicket');
        return
    }

    if(classBook =="Economy" || classBook =="Business" ){

    }
    else{
        alert('Enter business or economy class only!');
    }


    $.post("/calculatecost",
    {'flight_id':flight_id,'numtickets':numTicket,'classBook':classBook},
    function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
        var obj = JSON.parse(data)
        console.log(obj)
       // window.costrec = obj[0];
        console.log(obj)
        var cost = document.getElementById("price");

        cost.innerHTML = 'Total cost(INR): '+obj.data1;

        if(obj.data2 != "0")
        {
            cost.innerHTML = 'Total cost(INR): '+obj.data1 +"<br/>"+'Discount applied : '+obj.data2;
        }
    });


    

}

function confirmClick(){

    var flight_id = document.getElementById("flightid").value;
    var classBook = document.getElementById("classbooking").value;
    var numTicket = document.getElementById("numberticket").value;

    var username = "suhas";
	//json_={"name":name,"qty":qty,"type":option}
	var request=new XMLHttpRequest();

	request.onreadystatechange=function(){
        if(request.readyState===XMLHttpRequest.DONE){
            if(request.status===200)
            {
                alert('Updated Successfully');
            }
            else{
                alert('Network Error');
            }
            
    }
    };
    request.open("POST",'http://localhost:5000/confirmbooking',true);
    request.setRequestHeader('Content-Type','application/json');
    request.send(JSON.stringify({id:flight_id,class:classBook,username:username,numtickets:numTicket}));

    console.log("Inside confirm click");



}

function pastbookings(){
 
    var container = document.getElementById("maincontainer");

    $.get("/retrieveTickets",
    
    function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
       
       

    });

    container.innerHTML = null;

    var htmlnew = `<h3>Your past bookings</h3>
    <div id = "ticket1" class="card">
            <h5 class="card-header">Bangalore - Mumbai</h5>
            <div class="card-body">
              <h5 class="card-title">15th August 2018</h5>
                <br>
              <button onclick="reviewExperience()" type = "button" class="btn btn-primary" >Review the experience</button>
            </div>
        </div>
        <div id = "ticket2" class="card">
                <h5 class="card-header">Mumbai - Delhi</h5>
                <div class="card-body">
                  <h5 class="card-title">10th January 2017</h5>
                    <br>
                  <button onclick="reviewExperience()" type = "button" class="btn btn-primary" >Review the experience</button>
                </div>
            </div>`;
    container.innerHTML = htmlnew;

}

function reviewExperience(){

    var container = document.getElementById("maincontainer");

    container.innerHTML = null;

    var htmlnew = `<div >
    <form id="reviewform" action="/submitreview" method="POST">
      <!-- Change starability-basic to different class to see animations. -->
      <fieldset class="starability-basic">
        <h4 style="width:300px">Rate the experience</h4>
        <input type="radio" id="no-rate" class="input-no-rate" name="rating" value="0" checked aria-label="No rating." />
  
        <input type="radio" id="rate1" name="rating" value="1" />
        <label for="rate1">1 star.</label>
  
        <input type="radio" id="rate2" name="rating" value="2" />
        <label for="rate2">2 stars.</label>
  
        <input type="radio" id="rate3" name="rating" value="3" />
        <label for="rate3">3 stars.</label>
  
        <input type="radio" id="rate4" name="rating" value="4" />
        <label for="rate4">4 stars.</label>
  
        <input type="radio" id="rate5" name="rating" value="5" />
        <label for="rate5">5 stars.</label>
  
        <span class="starability-focus-ring"></span>
      </fieldset>
    
</div>
<h4 style="width:800px">Tell us more about your experience</h4>

<textarea style=" height: 200px;" name="reviewparagraph" type="text" form="reviewform" class="form-control" id="usr"></textarea>
<br>
<button form="reviewform" style="background-color:darkorchid; color: white" type="submit" class="btn btn-default" onclick="submitreview()">Submit</button>
</form>
</div>`;

    container.innerHTML = htmlnew;


}

function getreviewsclick(){
   
    var flightid = document.getElementById("flightid").value;
    console.log(flightid);

    var request=new XMLHttpRequest();

	request.onreadystatechange=function(){
        if(request.readyState===XMLHttpRequest.DONE){
            if(request.status===200)
            {
                callback(this)
                alert('Updated Successfully');
            }
            else{
                alert('Network Error');
            }
            
    }
    };
    request.open("POST",'http://localhost:5000/retrieveReviews',true);
    request.setRequestHeader('Content-Type','application/json');
    request.send(JSON.stringify({flight_id:flightid}));
}

function callback(request)

{
    json_returned = request.response;

    var json_obj = JSON.parse(json_returned)

    console.log(JSON.stringify({flight_id:flightid}));
    console.log(JSON.parse(json_returned) );

    var container_table = document.getElementById("tablebody");
    container_table.innerHTML = json_obj.data;

}

function submitreview(){
    alert('Your review was submmitted sucessfully');
  
}

function manageReviews(){

    var container = document.getElementById("admincontainer");

    container.innerHTML = null;
    var htmlnew =` <h4>Enter Flight ID</h4>
                   
    <input id="flightid" style="padding:5px" type="text">
    <button onclick="getreviewsclick()" class="btn btn-primary" >Get reviews</button>
    <div class="card-body table-responsive">
                                <table class="table table-hover table-striped"> 
                                    <col width='300'>                                           
                              <thead>                               
                                  <th>Rating</th>
                                  <th>Review</th>                                                                                              
                             </thead>
                              <tbody id="tablebody">
                             </tbody>
                            </table>
                        </div>`;

    container.innerHTML = htmlnew;


}

function registerSubmit(){
   
    var name = document.forms["regForm"]["name"].value;
    var username = document.forms["regForm"]["username"].value;
    var password = document.forms["regForm"]["password"].value;
    var repassword = document.forms["regForm"]["repassword"].value;
    var bday = document.forms["regForm"]["birthday"].value;
    var email = document.forms["regForm"]["email"].value;
    var phone = document.forms["regForm"]["phone"].value;
    var gender  = document.forms["regForm"]["gender"].value;

        
    if (name == "") {
        alert("Name must be filled out");
        return false;
    }
    if (username == "") {
        alert("UserName must be filled out");
        return false;
    }
    if (password == "") {
        alert("Password must be filled out");
        return false;
    }
    if (repassword == "") {
        alert("Renter password");
        return false;
    }
    if (phone == "") {
        alert("Number must be filled out");
        return false;
    }
    if (email == "") {
        alert("Email must be filled out");
        return false;
    }
    if(password != repassword){
        alert('passwords must be the same');
        return false;
    }
    console.log(name,username,password,repassword,bday.toString(),gender,email)

   

    $.post("/registrationClick",
    {'name':name,'username':username,'password':password,'birthday':bday.toString(),'gender':gender,'email':email,'phone':phone},
    function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
        window.location.href = "/";
        
    });

    
    

    return false;
}
