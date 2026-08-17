/**
 * AyurShakti Email Marketing System
 * ==================================
 * Deploy this file in Google Apps Script Editor attached to the Sheet.
 * 
 * Sheet: AyurShakti Email List
 * Spreadsheet ID: 1-8SFDK23ZXMGKmBfdXpY-wNkwTGWZfTUTy9JJPZAZas
 * 
 * Triggers to set up (run installTriggers() once):
 *   1. On form submit → sendWelcomeEmail(e)
 *   2. Weekly Tuesday 8am → sendWeeklyNewsletter()
 */

var CONFIG = {
  SHEET_NAME: 'AyurShakti Email List',
  LEAD_MAGNET_URL: 'https://resources.ayurshakti.shop/pdfs/lead-magnet.pdf',
  LEAD_MAGNET_TITLE: '5 Ayurvedic Home Remedies for Common Pet Ailments',
  BLOG_URL: 'https://www.ayurshakti.shop',
  BLOG_NAME: 'AyurShakti',
  OWNER_NAME: 'Suresh Bhati',
  OWNER_EMAIL: 'contact@ayurshakti.shop',
  MAX_DAILY_EMAILS: 80,
  UNSUBSCRIBE_BOUNCE_LIMIT: 3
};

var COL = {
  TIMESTAMP: 0,
  NAME: 1,
  EMAIL: 2,
  SOURCE: 3,
  LEAD_SENT: 4,
  UNSUBSCRIBED: 5,
  UNSUBSCRIBED_AT: 6,
  LAST_NEWSLETTER: 7,
  BOUNCE_COUNT: 8
};

/**
 * ============================================================
 * INSTALLATION
 * ============================================================
 */

function installTriggers() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  
  TriggerApp.deleteTriggers(sheet);
  
  ScriptApp.newTrigger('sendWelcomeEmail')
    .forSpreadsheet(sheet)
    .onFormSubmit()
    .create();
  
  ScriptApp.newTrigger('sendWeeklyNewsletter')
    .timeBased()
    .onWeekDay(CONFIG.WEEKLY_SEND_DAY || 2)
    .atHour(CONFIG.WEEKLY_SEND_HOUR || 8)
    .create();
  
  ScriptApp.newTrigger('checkBounces')
    .timeBased()
    .everyDays(1)
    .atHour(6)
    .create();
  
  Logger.log('Triggers installed successfully');
}

function deleteAllTriggers_() {
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(t) { ScriptApp.deleteTrigger(t); });
  Logger.log('All triggers deleted');
}

/**
 * ============================================================
 * WELCOME EMAIL (Trigger: On Form Submit)
 * ============================================================
 */

function sendWelcomeEmail(e) {
  try {
    var row = e.range.getRow();
    var sheet = e.source.getSheetByName(CONFIG.SHEET_NAME);
    
    var name = sheet.getRange(row, COL.NAME + 1).getValue();
    var email = sheet.getRange(row, COL.EMAIL + 1).getValue();
    
    if (!email) return;
    
    var subject = 'Welcome to AyurShakti — Your Free Guide Inside!';
    var body = buildWelcomeBody_(name);
    
    var unsubscribeUrl = getUnsubscribeUrl_(email);
    var bodyWithFooter = body + '\n\n---\nTo unsubscribe: ' + unsubscribeUrl;
    
    GmailApp.sendEmail(email, subject, bodyWithFooter, {
      name: CONFIG.OWNER_NAME,
      from: CONFIG.OWNER_EMAIL
    });
    
    sheet.getRange(row, COL.LEAD_SENT + 1).setValue(true);
    Logger.log('Welcome email sent to: ' + email);
  } catch (err) {
    Logger.log('Error in sendWelcomeEmail: ' + err.message);
  }
}

function buildWelcomeBody_(name) {
  return [
    'Hi ' + name + ',',
    '',
    'Welcome to the AyurShakti community! I\'m ' + CONFIG.OWNER_NAME + ', and I\'m thrilled to have you here.',
    '',
    'As promised, here\'s your free guide:',
    CONFIG.LEAD_MAGNET_URL,
    '',
    'This guide covers "' + CONFIG.LEAD_MAGNET_TITLE + '" that you can start using today.',
    '',
    'What to expect next:',
    '- Weekly Ayurveda tips and articles in your inbox',
    '- Evidence-based natural remedies for humans and pets',
    '- Early access to new research and guides',
    '',
    'Stay healthy,',
    CONFIG.OWNER_NAME,
    CONFIG.BLOG_URL,
    '',
    'P.S. Add me to your contacts so my emails don\'t land in spam!'
  ].join('\n');
}

/**
 * ============================================================
 * WEEKLY NEWSLETTER (Trigger: Time-based, Weekly)
 * ============================================================
 */

function sendWeeklyNewsletter() {
  var articles = fetchLatestArticles_();
  if (!articles || articles.length === 0) {
    Logger.log('No articles found for newsletter');
    return;
  }
  
  var subscribers = getActiveSubscribers_();
  if (subscribers.length === 0) {
    Logger.log('No active subscribers');
    return;
  }
  
  var dateStr = Utilities.formatDate(new Date(), 'EST', 'yyyy-MM-dd');
  var subject = 'This Week in Ayurveda — ' + dateStr;
  
  var sentCount = 0;
  for (var i = 0; i < subscribers.length; i++) {
    if (sentCount >= CONFIG.MAX_DAILY_EMAILS) {
      Logger.log('Reached daily limit of ' + CONFIG.MAX_DAILY_EMAILS);
      break;
    }
    
    var sub = subscribers[i];
    var body = buildNewsletterBody_(sub.name, articles, dateStr);
    var unsubscribeUrl = getUnsubscribeUrl_(sub.email);
    var bodyWithFooter = body + '\n\n---\nTo unsubscribe: ' + unsubscribeUrl;
    
    try {
      GmailApp.sendEmail(sub.email, subject, bodyWithFooter, {
        name: CONFIG.OWNER_NAME,
        from: CONFIG.OWNER_EMAIL
      });
      
      updateNewsletterSent_(sub.row);
      sentCount++;
      Logger.log('Newsletter sent to: ' + sub.email);
    } catch (err) {
      Logger.log('Failed to send to ' + sub.email + ': ' + err.message);
      incrementBounce_(sub.row);
    }
    
    if (sentCount % 50 === 0) {
      Utilities.sleep(1000);
    }
  }
  
  Logger.log('Newsletter complete: ' + sentCount + ' emails sent');
}

function buildNewsletterBody_(name, articles, dateStr) {
  var lines = [
    'Hi ' + name + ',',
    '',
    'Here are this week\'s top articles from ' + CONFIG.BLOG_NAME + ':',
    ''
  ];
  
  for (var i = 0; i < articles.length; i++) {
    var a = articles[i];
    var url = a.url + '?utm_source=email&utm_medium=newsletter&utm_campaign=weekly-' + dateStr + '&utm_content=article-' + (i + 1);
    lines.push((i + 1) + '. ' + a.title.toUpperCase());
    lines.push('   ' + a.snippet);
    lines.push('   Read more: ' + url);
    lines.push('');
  }
  
  lines.push('Wishing you wellness,');
  lines.push(CONFIG.OWNER_NAME);
  lines.push(CONFIG.BLOG_URL);
  
  return lines.join('\n');
}

function fetchLatestArticles_() {
  try {
    var url = CONFIG.BLOG_URL + '/atom.xml';
    var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var xml = response.getContentText();
    
    var entries = xml.match(/<entry>[\s\S]*?<\/entry>/g);
    if (!entries) return [];
    
    var articles = [];
    var count = 0;
    
    for (var i = 0; i < entries.length && count < 3; i++) {
      var titleMatch = entries[i].match(/<title[^>]*>([\s\S]*?)<\/title>/);
      var linkMatch = entries[i].match(/<link[^>]*href='([^']+)'/);
      var contentMatch = entries[i].match(/<content[^>]*>([\s\S]*?)<\/content>/);
      
      if (titleMatch && linkMatch) {
        var title = titleMatch[1].replace(/<[^>]+>/g, '').trim();
        var link = linkMatch[1].replace(/&amp;/g, '&');
        var snippet = '';
        
        if (contentMatch) {
          snippet = contentMatch[1].replace(/<[^>]+>/g, '').substring(0, 150).trim() + '...';
        }
        
        articles.push({ title: title, url: link, snippet: snippet });
        count++;
      }
    }
    
    return articles;
  } catch (err) {
    Logger.log('Error fetching articles: ' + err.message);
    return [];
  }
}

function getActiveSubscribers_() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  var data = sheet.getDataRange().getValues();
  var subscribers = [];
  
  for (var i = 1; i < data.length; i++) {
    var email = data[i][COL.EMAIL];
    var unsubscribed = data[i][COL.UNSUBSCRIBED];
    var bounceCount = data[i][COL.BOUNCE_COUNT] || 0;
    
    if (email && !unsubscribed && bounceCount < CONFIG.UNSUBSCRIBE_BOUNCE_LIMIT) {
      subscribers.push({
        row: i + 1,
        name: data[i][COL.NAME] || 'Reader',
        email: email
      });
    }
  }
  
  return subscribers;
}

/**
 * ============================================================
 * CUSTOM EMAIL (Manual — Run from Editor)
 * ============================================================
 */

function sendCustomEmail() {
  var ui = SpreadsheetApp.getUi();
  var subject = ui.prompt('Subject:', ui.ButtonSet.OK_CANCEL);
  if (subject.getSelectedButton() !== ui.Button.OK) return;
  
  var body = ui.prompt('Email Body (plain text):', ui.ButtonSet.OK_CANCEL);
  if (body.getSelectedButton() !== ui.Button.OK) return;
  
  var subscribers = getActiveSubscribers_();
  if (subscribers.length === 0) {
    ui.alert('No active subscribers');
    return;
  }
  
  var sentCount = 0;
  for (var i = 0; i < subscribers.length; i++) {
    if (sentCount >= CONFIG.MAX_DAILY_EMAILS) break;
    
    var sub = subscribers[i];
    var personalBody = 'Hi ' + sub.name + ',\n\n' + body.getResponseText();
    var unsubscribeUrl = getUnsubscribeUrl_(sub.email);
    var bodyWithFooter = personalBody + '\n\n---\nTo unsubscribe: ' + unsubscribeUrl;
    
    try {
      GmailApp.sendEmail(sub.email, subject.getResponseText(), bodyWithFooter, {
        name: CONFIG.OWNER_NAME,
        from: CONFIG.OWNER_EMAIL
      });
      sentCount++;
    } catch (err) {
      Logger.log('Failed: ' + sub.email + ' - ' + err.message);
      incrementBounce_(sub.row);
    }
  }
  
  ui.alert('Sent to ' + sentCount + ' subscribers');
}

/**
 * ============================================================
 * UNSUBSCRIBE
 * ============================================================
 */

function addUnsubscribe(email) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  var data = sheet.getDataRange().getValues();
  
  for (var i = 1; i < data.length; i++) {
    if (data[i][COL.EMAIL] === email) {
      var row = i + 1;
      sheet.getRange(row, COL.UNSUBSCRIBED + 1).setValue(true);
      sheet.getRange(row, COL.UNSUBSCRIBED_AT + 1).setValue(new Date());
      Logger.log('Unsubscribed: ' + email);
      return true;
    }
  }
  return false;
}

function getUnsubscribeUrl_(email) {
  var scriptUrl = ScriptApp.getService().getUrl();
  return scriptUrl + '?action=unsubscribe&email=' + encodeURIComponent(email);
}

/**
 * ============================================================
 * BOUNCE HANDLING
 * ============================================================
 */

function checkBounces() {
  var threads = GmailApp.search('in:inbox from:mailer-daemon@googlemail.com is:unread');
  
  for (var t = 0; t < threads.length; t++) {
    var messages = threads[t].getMessages();
    for (var m = 0; m < messages.length; m++) {
      var body = messages[m].getPlainBody();
      var emailMatch = body.match(/<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>/);
      
      if (emailMatch) {
        var bouncedEmail = emailMatch[1];
        var row = findRowByEmail_(bouncedEmail);
        
        if (row) {
          incrementBounce_(row);
          Logger.log('Bounce recorded for: ' + bouncedEmail);
        }
      }
    }
    threads[t].markRead();
  }
}

function findRowByEmail_(email) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  var data = sheet.getDataRange().getValues();
  
  for (var i = 1; i < data.length; i++) {
    if (data[i][COL.EMAIL] === email) {
      return i + 1;
    }
  }
  return null;
}

function incrementBounce_(row) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  var current = sheet.getRange(row, COL.BOUNCE_COUNT + 1).getValue() || 0;
  sheet.getRange(row, COL.BOUNCE_COUNT + 1).setValue(current + 1);
  
  if (current + 1 >= CONFIG.UNSUBSCRIBE_BOUNCE_LIMIT) {
    sheet.getRange(row, COL.UNSUBSCRIBED + 1).setValue(true);
    sheet.getRange(row, COL.UNSUBSCRIBED_AT + 1).setValue(new Date());
    Logger.log('Auto-unsubscribed after bounces: row ' + row);
  }
}

function updateNewsletterSent_(row) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  sheet.getRange(row, COL.LAST_NEWSLETTER + 1).setValue(new Date());
}

/**
 * ============================================================
 * WEB APP — Unsubscribe Handler
 * ============================================================
 */

function doGet(e) {
  var action = e.parameter.action;
  var email = e.parameter.email;
  
  if (action === 'unsubscribe' && email) {
    addUnsubscribe(email);
    return HtmlService.createHtmlOutput(
      '<html><body style="font-family:sans-serif;text-align:center;padding:40px;">' +
      '<h2>You have been unsubscribed</h2>' +
      '<p>' + email + ' has been removed from our mailing list.</p>' +
      '<p>If this was a mistake, you can re-subscribe on our website.</p>' +
      '<p><a href="' + CONFIG.BLOG_URL + '">Visit AyurShakti</a></p>' +
      '</body></html>'
    );
  }
  
  return HtmlService.createHtmlOutput(
    '<html><body style="font-family:sans-serif;text-align:center;padding:40px;">' +
    '<h2>AyurShakti Email Service</h2>' +
    '<p>This endpoint handles email unsubscribe requests.</p>' +
    '</body></html>'
  );
}

/**
 * ============================================================
 * TEST / DEBUG
 * ============================================================
 */

function sendTestWelcome() {
  var name = CONFIG.OWNER_NAME;
  var email = CONFIG.OWNER_EMAIL;
  
  var subject = '[TEST] Welcome to AyurShakti';
  var body = buildWelcomeBody_(name);
  var unsubscribeUrl = getUnsubscribeUrl_(email);
  var bodyWithFooter = body + '\n\n---\nTo unsubscribe: ' + unsubscribeUrl;
  
  GmailApp.sendEmail(email, subject, bodyWithFooter, {
    name: CONFIG.OWNER_NAME,
    from: CONFIG.OWNER_EMAIL
  });
  
  Logger.log('Test welcome email sent to: ' + email);
}

function testFetchArticles() {
  var articles = fetchLatestArticles_();
  Logger.log('Articles found: ' + (articles ? articles.length : 0));
  articles.forEach(function(a, i) {
    Logger.log((i + 1) + '. ' + a.title + ' -> ' + a.url);
  });
}

function testCountSubscribers() {
  var subs = getActiveSubscribers_();
  Logger.log('Active subscribers: ' + subs.length);
}

/**
 * ============================================================
 * UTILITY — Delete old triggers helper for installTriggers
 * ============================================================
 */

var TriggerApp = {
  deleteTriggers: function(sheet) {
    var triggers = ScriptApp.getProjectTriggers();
    triggers.forEach(function(t) {
      if (t.getTriggerSourceId() === sheet.getId() ||
          t.getHandlerFunction() === 'sendWeeklyNewsletter' ||
          t.getHandlerFunction() === 'checkBounces') {
        ScriptApp.deleteTrigger(t);
      }
    });
  }
};
