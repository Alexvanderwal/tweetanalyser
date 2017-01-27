/**
 * Created by Alex on 26-11-2016.
 */
$(document).ready(function() {
    var sum = 0;
    var isStreaming = false;
    var uniqueUserID = '';
    var dataUpdater = null;
    var posScore = 0, negScore = 0, neutScore = 0;
    //Here we are using the javascript to get the DOM object instead of a reference to the DOM object
    var btn = document.getElementById("button");
    var hashtag = document.getElementById("hashtag");
    //This will be the canvas we are feeding the chart into
    var ctx = document.getElementById("pieChart");
    var types = ['bar', 'pie', 'line', ''];
    fetchOldStreamData();

    function fetchOldStreamData(){
        if(!oldStreamData) {
            var oldStreamData = new XMLHttpRequest();
            oldStreamData.addEventListener('load', makeOldStreamIndex);
        }
        oldStreamData.open('GET', 'oldqueries/', false);
        oldStreamData.send();
    }


    function makeOldStreamIndex(){
        var responseData = JSON.parse(this.responseText);
        html = '<h5>Oude streams hervatten</h5>';
        for(var i = 0; i < responseData.length; i++){
            var hashtag = responseData[i].hashtag;
            html += '<div class="row">';
            html += '<div class="col s12 m6">';
            html += '<div class="card blue-grey darken-1">';
            html += '<div class="card-content white-text">';
            html += '<span class="card-title">'+ hashtag + '</span>';
            html += '<p>Aantal tweets '+responseData[i].tweet_amount+'</p>';
            html += '<p>sentiment '+responseData[i].avg_sentiment+'</p>';
            html += '</div> <div class="card-action"> <a id="card" name="'+hashtag+'">Open de stream</a>';
            html += '</div> </div> </div>';
        }
        document.getElementById("cards").innerHTML = html;

        $("a").click(function(){
        if(isStreaming == false) {
            startStream($(this).attr("name"));
        }
        else {endStream();}

    });
    }

    var data = {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [{
            data: [100, 100, 100],
            backgroundColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(255,99,132, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
        }]
    };

    var options = {};


    var dynamicChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });
    dynamicChart.update();


    btn.addEventListener('click', function (event){
        if(!isStreaming) {
            hashtag = encodeURIComponent($("#hashtag").val().toLowerCase());
            startStream(hashtag);
        }
        else {
            endStream();
        }
    });

    function endStream(){
        isStreaming = false;
        var endStream = new XMLHttpRequest();
        endStream.open("GET", 'stop/stream/' + uniqueUserID);
        endStream.send();
        $("#button").val("Voer de zoekquery uit");
        clearInterval(dataUpdater);
          var oldStreamData = new XMLHttpRequest();
    oldStreamData.addEventListener('load', makeOldStreamIndex);
    oldStreamData.open('GET', 'oldqueries/', false);
    oldStreamData.send();

        neutScore = 0;
        posScore = 0;
        negScore = 0;
    }

    function startStream(hashtag){
        isStreaming = true;
        $("#button").val("zet de stream uit");
        var activeStream = new XMLHttpRequest();
        uniqueUserID = createUUID();
        activeStream.open('GET', 'stream/' + uniqueUserID + '/' + hashtag.toLowerCase(), false);
        activeStream.send();


        dataUpdater = setInterval(function(){
            var updateStream = new XMLHttpRequest();
            updateStream.addEventListener('load', updateData);
            updateStream.open('GET', 'update/' + uniqueUserID);
            updateStream.send();
        },2000);
    }

    function createUUID(){
        return uuid.v1(); // -> v1 UUID
    }
    function updateData(){
        var responseData = JSON.parse(this.responseText);
        posScore = responseData.pos_tweet_amount;
        negScore = responseData.neg_tweet_amount;
        neutScore = responseData.neut_tweet_amount;
        adjustScore();


    }
    function adjustScore(){
        sum = neutScore + negScore + posScore;
        data.datasets[0].data[0] = posScore;
        data.datasets[0].data[1] = negScore;
        data.datasets[0].data[2] = neutScore;
        dynamicChart.update();
        $("#tweetAnalyzed").html('Total tweets analyzed: ' + sum);
    }

    window.onbeforeunload = function(){
        //Make sure all streams are killed when the user leaves the webpage
        if(isStreaming){
            endStream();
        }
    }
});