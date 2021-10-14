 function Redirect()
    {
        window.location="{% url 'home' %}";
    }
    document.write("You will be redirected to a new page in 5 seconds");
    setTimeout('Redirect()', 5000);