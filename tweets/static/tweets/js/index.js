/**
 * Created by Alex on 26-11-2016.
 */
$(function() {
    var sum = 0;
    var isStreaming = false;
    var btn = document.getElementById("button");
    var hashtag = document.getElementById("hashtag");
    var uniqueUserID = '';
    //This will be the canvas we are feeding the chart into
    var ctx = document.getElementById("pieChart");
    var data = {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [{
            data: [12, 19, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderColor: [
                'rgba(255,99,132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
        }]
    };

    var options = {};


    var pieChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });


    btn.addEventListener('click', function (event){
        if(!isStreaming) {
            hashtag = encodeURIComponent($("#hashtag").val());
            startStream(hashtag);
            $('#alertbox').toggle();
        }
        else {
            endStream()
        }
    });

    function endStream(){
        isStreaming = false;
        var endStream = new XMLHttpRequest();
        endStream.open("GET", 'stop/stream/' + uniqueUserID);
        endStream.send()
    }

    function startStream(hashtag){
        isStreaming = true;
        var StartStream = new XMLHttpRequest();
        StartStream.addEventListener('load', function () {
            isAnalyzing = true;
        });
        uniqueUserID = createUUID();
        StartStream.open('GET', 'stream/' + uniqueUserID + '/' + hashtag );
        StartStream.send();
    }

    function createUUID(){
        return uuid.v1(); // -> v1 UUID
    }

    function adjustScore(){
        sum = 0;
         for( var i = 0, len = pieChart.data.datasets[0].data.length;i < len; i++){
            sum += pieChart.data.datasets[0].data[i];
             pieChart.data.datasets[0].data[i] = 15;
         }
        document.getElementById("tweetAnalyzed").innerHTML = 'Total tweets analyzed: ' + sum;
    }

    window.onbeforeunload = function(){
        //Make sure all streams are killed when the user leaves the webpage
        if(isStreaming){
            endStream();
        }
    }

});