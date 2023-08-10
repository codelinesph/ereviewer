function exportToExcel(tableId){
    var tab_text="<table border='1px'><tr bgcolor='#ffffff'>";
    var textRange; var j=0;
    tab = document.getElementById(tableId); // id of table

    for(j = 0 ; j < tab.rows.length ; j++){
        tab_text=tab_text+tab.rows[j].innerHTML+"</tr>";
    }

    tab_text=tab_text+"</table>";
    tab_text= tab_text.replace(/<a[^>]*>|<\/a>/g, "");//remove if u want links in your table
    tab_text= tab_text.replace(/<img[^>]*>/gi,""); // remove if u want images in your table
    tab_text= tab_text.replace(/<input[^>]*>|<\/input>/gi, ""); // reomves input params

    var ua = window.navigator.userAgent;
    var msie = ua.indexOf("MSIE "); 

    if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./)){
        txtArea1.document.open("txt/html","replace");
        txtArea1.document.write(tab_text);
        txtArea1.document.close();
        txtArea1.focus(); 
        sa=txtArea1.document.execCommand("SaveAs",true,"Say Thanks to Submit.xls");
    }  
    else sa = window.open('data:application/vnd.ms-excel,' + encodeURIComponent(tab_text));  
    return (sa);
}