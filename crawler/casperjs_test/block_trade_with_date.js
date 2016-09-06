/**
 * for specific crawl date, you must find that date.
 */

var securitiesDatas = [],
    bondDatas = [],
    url = 'http://www.sse.com.cn/disclosure/diclosure/block/';

var startPage = 1;
var endPage = 1;

var fs = require('fs');
var casper = require('casper').create();
var st_flag = casper.cli.has('st_date'),
    ed_flag = casper.cli.has('ed_date'),
    startPageFlag = casper.cli.has('st_page'),
    endPageFlag = casper.cli.has('ed_page');

var outFile = casper.cli.get('outfile');

function extract(info_selector){
    var perValue = casper.evaluate(function(table_selector){
        var values = [];
        $(table_selector).find('tr').slice(1).each(function(){
            var items = [];
            $(this).find('td').each(function(){
                var txt = $(this).text().replace(/,|\s/g, '');
                // var toUnicode = escape(txt).replace(/%/g, "\\").toLowerCase();
                items.push(txt);
            });

            values.push(items);
        });
        return values;
    }, info_selector);

    if (info_selector == '#bulktrade_one_div'){
        perValue.forEach(function(item, index, array){
            securitiesDatas.push(item);
        });
    } else {
        perValue.forEach(function(item, index, array){
            bondDatas.push(item);
        });
    }

}

/* Note that:
* (1): 'for loop' statement don't use,
* (2): but sometimes `if` statement also in casper environment,
*/
function getPages(index) {
    return casper.evaluate(function(eqInd){
        var regex = /(\d+)/g,
            t = $('.paging_input').eq(eqInd).text();

        if (regex.test(t)){
            return parseInt(RegExp.$1);
        }
        return 0;
    }, index);
}

function dateText(selector){
    return casper.evaluate(function(select){
        return $(select).val();
    }, selector);

}


function loop(){
    extract('#bulktrade_one_div');
    extract('#bulktrade_two_div');

    this.echo('stPage11111:' + startPage);
    if(startPage < endPage){
        startPage++;
        this.sendKeys('#bulktrade_container_pageid', '' + startPage);
        this.click('#bulktrade_container_togo');
        this.wait(10000);
        this.run(loop);
    } else {
        fs.write('D:/temp/data/sha/' + outFile +'.txt',
            JSON.stringify({"sf_data": securitiesDatas, "bond_data": bondDatas}), 'w');
        this.exit();
    }
}


casper.start(url);

casper.waitForSelector('input[target="bulktradehisinfodate"]', function () {
        this.click('input[target="bulktradehisinfodate"]')
}, function(){this.echo('click input[target="bulktradehisinfodate"] error.');}, 30000);

if (st_flag) {
    var queryStartDate = casper.cli.get('st_date').split('-');
    var st_year = queryStartDate[0],
        st_month = queryStartDate[1];

    casper.echo('st:' + (typeof st_year) + ' ' + (typeof st_month));
    casper.echo('ss:' + 'td[onclick="day_Click(' + queryStartDate.join(',') + ');"]');

    casper.waitForSelector('#bulktradestartdate', function () {
        this.click('#bulktradestartdate')
    }, function(){this.echo('Query start date timeout');}, 30000);

    casper.withFrame(0, function() {
        this.sendKeys('#dpTitle > div:nth-child(3) > input', st_month);
        this.sendKeys('#dpTitle > div:nth-child(4) > input', st_year);
        this.wait(5000);
        this.click('td[onclick="day_Click(' + queryStartDate.join(',') + ');"]');
    });

    if (!ed_flag) {
        casper.withFrame(-1, function() {
            this.click('#bulktradehisinfodate input[type="image"]');
            this.wait(10000);
            this.echo('start date text:' + dateText('#bulktradestartdate'));
        });
    } else {
        casper.withFrame(-1, function() {
            this.wait(10000);
            this.echo('start date text:' + dateText('#bulktradestartdate'));
        });
    }
}

if (ed_flag){
    var queryEndDate = casper.cli.get('ed_date').split('-');
    var ed_year = queryEndDate[0],
        ed_month = queryEndDate[1];

    casper.waitForSelector('#bulktradeenddate', function () {
        this.click('#bulktradeenddate')
    }, function(){this.echo('Query end date timeout');}, 30000);

    casper.withFrame(0, function() {
        this.sendKeys('#dpTitle > div:nth-child(3) > input', ed_month);
        this.sendKeys('#dpTitle > div:nth-child(4) > input', ed_year);
        this.wait(5000);
        this.click('td[onclick="day_Click(' + queryEndDate.join(',') + ');"]');
    });

    casper.withFrame(-1, function() {
        this.click('#bulktradehisinfodate input[type="image"]');
        this.wait(5000);
        this.echo('end date text:' + dateText('#bulktradeenddate'));
    });
}

casper.waitForSelector('#aaabbbccc', function(){
    //this.echo(this.getHTML());
}, function(){
    //this.echo(this.getHTML());
    if (startPageFlag){
        startPage = casper.cli.get('st_page');
    } else {
        startPage = 1;

    }

    if (!endPageFlag) {
        endPage = getPages(0);
    } else {
        endPage = casper.cli.get('ed_page');
    }
    this.echo('endPage:' + endPage);
}, 30000);

casper.run(loop);

