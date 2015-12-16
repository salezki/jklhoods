// Javascript source code
//asd
window.onload = function(){
    alustus();
    // twitteriStriimi(10);
    alustaInstagramit();
    alustaTwiitit();
    //instagramBlock(10);
    //fetchTweets();
    ajastin_twitter = setInterval(fetchTweets.bind(null, false), 5000);
	ajastin_instagram = setInterval(fetchInstagram.bind(null, false), 5000);
}


window.onresize = function(event) {
    setInstagramButton();
    setTwitterButton();
};


function alustus() {
    $("#show_twitter").click(show_twitter);
    $("#show_insta").click(show_instagram);
    $("#show_all").click(show_all);
    $("#drop_twitter").click(twitter_top_hastags);
    $("#drop_instagram").click(instagram_top_hastags);
    $("#uusia_twiitteja").click(function() {
        $(this).hide();
        fetchTweets(true);
    });
    $("#uusia_posteja").click(function() {
		$(this).hide();
        fetchInstagram(true);
    });
    $("#hae_seuraavat").click(haeSeuraavat_tweet);
	$("#hae_seuraavat_instagram").click(haeSeuraavat_instagram);
}


function peruuta_tagit_twitter() {
    clearInterval(ajastin_twitter);
    ajastin_twitter = setInterval(fetchTweets.bind(null, false), 5000);
    $("#hae_seuraavat").off("click");
    $("#hae_seuraavat").click(haeSeuraavat_tweet);
    $(".tweet").remove();
    alustaTwiitit();
    $("#uusia_twiitteja").off("click");
    $("#uusia_twiitteja").click(function() {
        $(this).hide();
        fetchTweets(true);
    });
}


//Show all feed
function show_all(e){
    e.preventDefault();
    $("#div_twitter").show();
    $("#div_insta").show();
    $("#div_insta").addClass("col-md-6");
    $("#div_twitter").addClass("col-md-6");
}


//Show only twitter feed
function show_twitter(e){
    e.preventDefault();
    $("#div_insta").hide();
    $("#div_twitter").show();
    $("#div_twitter").removeClass("col-md-6");
}


//Show only instagram feed
function show_instagram(e){
    e.preventDefault();
    $("#div_twitter").hide();
    $("#div_insta").show();
    $("#div_insta").removeClass("col-md-6")
}


function twitter_top_hastags(e) {
    e.preventDefault();
    $.post('/hashtags',
        function(data) {
            $("#twitter_top1").text(data.result[1]);
            $("#twitter_top2").text(data.result[2]);
            $("#twitter_top3").text(data.result[3]);
            $("#twitter_top4").text(data.result[4]);
            $("#twitter_top5").text(data.result[5]);
        });
}


function instagram_top_hastags(e) {
    e.preventDefault();
    $.post('/hashtags_insta',
        function(data) {
            $("#instagram_top1").text(data.result[1]);
            $("#instagram_top2").text(data.result[2]);
            $("#instagram_top3").text(data.result[3]);
            $("#instagram_top4").text(data.result[4]);
            $("#instagram_top5").text(data.result[5]);
        });
}



// =================================================================
// Instagram funktiot ==============================================
// =================================================================


function peruuta_tagit_instagram() {
    clearInterval(ajastin_instagram);
    ajastin_instagram = setInterval(fetchInstagram.bind(null, false), 5000);
    $("#hae_seuraavat_instagram").off("click");
    $("#hae_seuraavat_instagram").click(haeSeuraavat_instagram);
    $(".instapost").remove();
    alustaInstagramit();
    $("#uusia_posteja").off("click");
    $("#uusia_posteja").click(function() {
        $(this).hide();
        fetchInstagram(true);
    });
}


function alustaInstagramit() {
    $.ajax({
        method: "POST",
        url: '/alustaInstagrams',
        contentType: 'application/json',
        success: function(data) {
            for (var i = 9; i >= 0; i--) {
                var testi = '<div class="instapost" instacode="'+
                String(data.result[i])+'"></div>';
                $(testi).insertAfter( "#uusia_posteja" );
            };
            instagramBlock(10);
        }
    });
}


function instagramBlock(count) {
//    http://api.instagram.com/oembed?url=http://instagr.am/p/{shortcode}
// theUrl, callback
    var posts;
    if (count > 10) {
        posts = $(".instapost").slice(0,10);
        new_posts = 10;
    } else if (count < 0) {
        posts = $('.instapost').slice(count);
        new_posts = Math.abs(count);
    } else {
        posts = $(".instapost").slice(0,count);
        new_posts = count;
    };

    var Url = "//api.instagram.com/oembed?url=http://instagr.am/p/"
    posts.each(function(index){
        var shortcode = this.getAttribute("instacode");
        var theUrl = Url.concat(shortcode);
        var paikka = this;
        $.ajax({
            type: "GET",
            dataType: "jsonp",
            url: theUrl,
            success: function(response) {
                $(paikka).html($.parseHTML(response['html']));
                instgrm.Embeds.process();
            }
        });
    });
}


function fetchInstagram(jatka) {
    var posts = $(".instapost");
    var data = posts[0].getAttribute("instacode");
    $.ajax({
        method: "POST",
        url: '/fetchInstagram',
        contentType: 'application/json',
        data: JSON.stringify(String(data)),
        dataType: "json",
        success: function(data) {
            var count = data['result'].length;
            if (count > 0) {
                if (jatka === true) {
                    for (var i = 0; i < count; i++) {
                        var div = '<div class="instapost" instacode="'+
                        String(data.result[i])+'"></div>';
                        $(div).insertAfter( "#uusia_posteja" );
                        $(".instapost").slice(-1).remove();
                    };
                    instagramBlock(count);
                } else {
                    setInstagramButton();
                };
            }
        }
    });
}


function fetchTagInstagram(jatka, tagi) {
    var data = $(".instapost")[0].getAttribute("instacode");
    var send = {"tagi" : tagi, "shortcode" : data}
    $.ajax({
        method: "POST",
        url: '/fetchTagInstagram',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: "json",
        success: function(data) {
            var count = data['result'].length;
            if (count > 0) {
                if (jatka === true) {
                    for (var i = 0; i < count; i++) {
                        var div = '<div class="instapost" instacode="'+
                        String(data.result[i])+'"></div>';
                        $(div).insertAfter( "#uusia_posteja" );
                        $(".instapost").slice(-1).remove();
                    };
                    instagramBlock(count);
                } else {
                    $('#uusia_posteja').show();
                };
            }
        }
    });
}


function haeSeuraavat_instagram() {
    var data = $(".instapost:last")[0].getAttribute("instacode");
    $.ajax({
        method: "POST",
        url: '/haeSeuraavat_instagram',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data) {
            var count = data['result'].length;
            for (var i = 0; i < count; i++) {
                var div = '<div class="instapost" instacode="'+
                String(data.result[i])+'"></div>';
                $(div).insertBefore( "#hae_seuraavat_instagram" );
            };
            instagramBlock(-10);
        }
    });
}


function haeTagillaInsta(tagi) {
    send = {"tagi" : tagi};
    $.ajax({
        dataType: "json",
        method: "POST",
        url: "/hae_instagram_tagilla",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify(send),
        success: function(data) {
            $(".instapost").remove();
            var count = data['result'].length;
            for (var i = 0; i < count; i++) {
                var testi = '<div class="instapost" instacode="'+
                String(data.result[i])+'"></div>';
                $(testi).insertBefore( "#hae_seuraavat_instagram" );
            };
            instagramBlock(10);
            clearInterval(ajastin_instagram);
            ajastin_instagram = setInterval(fetchTagInstagram.bind(null, false, tagi), 5000);
            $("#uusia_posteja").off('click');
            $("#uusia_posteja").click( function (){
                $(this).hide();
                fetchTagInstagram(true, tagi);
            });
            $("#hae_seuraavat_instagram").off('click');
            $("#hae_seuraavat_instagram").click( function(){ haeSeuraavatTagilla_instagram(tagi); });
        }
    });
}


function haeSeuraavatTagilla_instagram(tagi){
    var data = $(".instapost:last")[0].getAttribute("instacode");
    send = {"tagi" : tagi, "instacode" : data};
    $.ajax({
        method: "POST",
        url: '/haes_instagram_tagilla',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: "json",
        success: function(data) {
            var count = data['result'].length;
            for (var i = 0; i < count; i++) {
                var div = '<div class="instapost" instacode="'+
                String(data.result[i])+'"></div>';
                $(div).insertBefore( "#hae_seuraavat_instagram" );
            };
            instagramBlock(-Math.abs(count));
        }
    });
}




// =================================================================
// Tweet funktiot ==================================================
// =================================================================


function alustaTwiitit() {
    $.ajax({
        method: "POST",
        url: '/alustaTweets',
        contentType: 'application/json',
        success: function(data) {
            for (var i = 9; i >= 0; i--) {
                var testi = '<div class="tweet" tweetID="'+
                String(data.result[i])+'"></div>';
                $(testi).insertAfter( "#uusia_twiitteja" );
            };
            twitteriStriimi(10);
        }
    });
}


function twitteriStriimi(count) {
    var tweets;
    if (count > 10) {
        tweets = $(".tweet").slice(0,10);
        new_tweets = 10;
    } else if (count < 0) {
        tweets = $('.tweet').slice(count);
        new_tweets = Math.abs(count);
    } else {
        tweets = $(".tweet").slice(0,count);
        new_tweets = count;
    };
    for (i = 0; i < new_tweets; i++) {
        var id = tweets[i].getAttribute("tweetID");
        twttr.widgets.createTweet(id, tweets[i],{
            conversation : 'none',    // or all
            cards        : 'visible',  // or visible 
            linkColor    : '#cc0000', // default is blue
            theme        : 'light'    // or dark
        });
    }; 
}


function fetchTweets(jatka) {
    var tweetit = $(".tweet");
    var data = tweetit[0].getAttribute("tweetID");
    $.ajax({
        method: "POST",
        url: '/fetchTweets',
        contentType: 'application/json',
        data: JSON.stringify(String(data)),
        dataType: "json",
        success: function(data) {
            var count = data['result'].length;
            if (count > 0) {
                if (jatka === true) {
                    for (var i = 0; i < count; i++) {
                        var testi = '<div class="tweet" tweetID="'+
                        String(data.result[i])+'"></div>';
                        $(testi).insertAfter( "#uusia_twiitteja" );
                        $(".tweet").slice(-1).remove();
                    };
                    twitteriStriimi(count);
                } else {
                    setTwitterButton();
                };
            };
        }
    });
}


function fetchTagTweets(jatka, tagi) {
    var data = $(".tweet")[0].getAttribute("tweetID");
    var send = {"tagi" : tagi, "tweetId" : data};
    $.ajax({
        method: "POST",
        url: '/fetchTagTweets',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: "json",
        success: function(data) {
            var count = data['result'].length;
            if (count > 0) {
                if (jatka === true) {
                    for (var i = 0; i < count; i++) {
                        var testi = '<div class="tweet" tweetID="'+
                        String(data.result[i])+'"></div>';
                        $(testi).insertAfter( "#uusia_twiitteja" );
                        $(".tweet").slice(-1).remove();
                    };
                    twitteriStriimi(count);
                } else {
                    $('#uusia_twiitteja').show();
                };
            };
        }
    });
}


function haeSeuraavat_tweet() {
    var data = $(".tweet:last")[0].getAttribute("tweetid");
    $.ajax({
        method: "POST",
        url: '/haeSeuraavat_tweet',
        contentType: 'application/json',
        data: JSON.stringify(String(data)),
        dataType: "json",
        success: function(data) {
            var count = data['result'].length;
            for (var i = 0; i < count; i++) {
                var testi = '<div class="tweet" tweetID="'+
                String(data.result[i])+'"></div>';
                $(testi).insertBefore( "#hae_seuraavat" );
            };
            twitteriStriimi(-Math.abs(count));
        }
    });
}


function haeTagilla_tweet(tagi) {
    send = {"tagi" : encodeURIComponent(tagi)};
	alert(encodeURIComponent(tagi));
    $.ajax({
        dataType: "json",
        method: "POST",
        url: "/hae_twitter_tagilla",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify(send),
        success: function(data) {
			alert("a");
            $(".tweet").remove();
            var count = data['result'].length;
			//alert(String(count));
            for (var i = 0; i < count; i++) {
                var testi = '<div class="tweet" tweetID="'+
                String(data.result[i])+'"></div>';
                $(testi).insertBefore( "#hae_seuraavat" );
            };
            twitteriStriimi(count);
            clearInterval(ajastin_twitter);
            ajastin_twitter = setInterval(fetchTagTweets.bind(null, false, tagi), 5000);
            $("#uusia_twiitteja").off('click');
            $("#uusia_twiitteja").click( function(){
                $(this).hide();
                fetchTagTweets(true, tagi);
            });
            $("#hae_seuraavat").off('click');
            $("#hae_seuraavat").click( function(){ haeSeuraavatTagilla_tweet(tagi); } );
        }
    });

}


function setInstagramButton() {

    var container = document.getElementsByClassName('instagram-media instagram-media-rendered');
    document.getElementById('uusia_posteja').setAttribute("style","width:" + container[0].offsetWidth + "px");
    $('#uusia_posteja').show();
}

function setTwitterButton() {
    var container = document.getElementsByClassName('twitter-tweet twitter-tweet-rendered');
    document.getElementById('uusia_twiitteja').setAttribute("style","width:" + container[0].offsetWidth + "px");
    $('#uusia_twiitteja').show();
}


function haeSeuraavatTagilla_tweet(tagi) {
    var data = $(".tweet:last")[0].getAttribute("tweetid");
    send = {"tagi" : tagi, "tweetId" : data};
    $.ajax({
        dataType: "json",
        method: "POST",
        url: "/haes_twitter_tagilla",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify(send),
        success: function(data) {
            var count = data['result'].length;
            for (var i = 0; i < count; i++) {
                var testi = '<div class="tweet" tweetID="'+
                String(data.result[i])+'"></div>';
                $(testi).insertBefore( "#hae_seuraavat" );
            };
            twitteriStriimi(-Math.abs(count));
        }
    });
}
