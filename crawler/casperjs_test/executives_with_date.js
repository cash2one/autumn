
var datas = [],
    url = 'http://www.sse.com.cn/disclosure/listedinfo/credibility/change/#';

var casper = require('casper').create();
var queryDate = casper.cli.get('date');
var changeDte = queryDate.split('-');
var year = changeDte[0],
    month = changeDte[1];
var page = 0,
    allPages = 0;


function extract(info_selector){
    var perValue = casper.evaluate(function(table_selector){
        var values = [];
        $(table_selector).find('tr').slice(1).each(function(){
            var items = [];
            $(this).find('td').each(function(){
                var txt = $(this).text().replace(/,|\s/g, '');
                 var toUnicode = escape(txt).replace(/%/g, "\\").toLowerCase();
                items.push(toUnicode);
            });

            values.push(items);
        });
        return values;
    }, info_selector);

    perValue.forEach(function(item, index, array){
        datas.push(item);
    });
}

function getPage(){
    return casper.evaluate(function () {
        var pageText = $('span.paging_input').text();
        var regexPage = /(\d+)/g;
        if (regexPage.test(pageText)){
            return parseInt(RegExp.$1);
        } else {
            return 0;
        }
    });
}

function loop(){
    extract('#gfbd_div_table');

    if(page < allPages){
        page++;
        this.sendKeys('#gfbd_div_table_pageid', '' + page);
        this.click('#gfbd_div_table_togo');
        this.wait(10000);
        this.run(loop);
    } else {
        this.echo(JSON.stringify({"data":datas})).exit();
    }
}

casper.start(url);


casper.waitForSelector('input#startDate', function () {
    this.echo('Now enter input ` start change date`');

    this.click('#startDate');
    this.wait(5000);

    this.withFrame(0, function () {
        this.sendKeys('#dpTitle > div:nth-child(4) > input', year);
        this.sendKeys('#dpTitle > div:nth-child(3) > input', month);
        this.wait(5000);
        this.click('td[onclick="day_Click(' + changeDte.join(',') + ');"]');
    });

    this.withFrame(-1, function(){
        this.wait(5000);
    })
}, function(){this.echo('input `start change date` error.');}, 30000);


casper.waitForSelector('input#endDate', function () {
    this.echo('Now enter input ` end change date`');

    this.click('#endDate');
    this.wait(5000);

    this.withFrame(0, function () {
        this.sendKeys('#dpTitle > div:nth-child(4) > input', year);
        this.sendKeys('#dpTitle > div:nth-child(3) > input', month);
        this.wait(5000);
        this.click('td[onclick="day_Click(' + changeDte.join(',') + ');"]');
    });

    this.withFrame(-1, function(){
        this.click('input#monthlySubmit');
        this.wait(5000);
    })
}, function(){this.echo('input `end change date` error.');}, 30000);


casper.then(function () {
    var st_ed_date = this.evaluate(function () {
        var st_date = $('#startDate').val();
        var ed_date = $('#endDate').val();
        return [st_date, ed_date]
    });

    this.echo('ultimate date:' + st_ed_date.join('->'))
});

casper.waitForSelector('#aaabbbccc', function(){},
    function(){
        allPages = getPage();
        this.echo('all pages:' + allPages)
    }, 30000);

casper.run(loop);
