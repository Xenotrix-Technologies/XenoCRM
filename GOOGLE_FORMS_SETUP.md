# Google Forms Integration Setup

This guide explains how to connect your Google Form to the XenoCRM system.

## Overview

Your Google Form submissions will automatically create leads in the CRM by sending data to the `/webhook/google-forms` endpoint.

## Google Form Structure

Your form should collect the following information:
- **Customer Name** (required)
- **Email** (required)
- **Phone** (optional)
- **Service** (optional)
- **Message** (optional)

## Setup Instructions

### Step 1: Open Your Google Form Script Editor

1. Open your Google Form: https://docs.google.com/forms/d/e/1FAIpQLSePrV30s32LfIl5YCBiAwAvWTMt-rj_WpKGhB-YgofGW8sw2w/edit
2. Click the three dots menu (⋮) in the top right
3. Select **Script editor**

### Step 2: Add the Integration Script

Copy and paste the following script into the editor:

```javascript
function onFormSubmit(e) {
  // Your CRM backend URL - UPDATE THIS WITH YOUR ACTUAL SERVER URL
  var webhookUrl = "http://localhost:8000/webhook/google-forms";
  
  // Get form responses
  var itemResponses = e.response.getItemResponses();
  
  // Initialize lead data
  var leadData = {
    customer_name: "",
    email: "",
    phone: "",
    service: "",
    message: ""
  };
  
  // Map form responses to lead data
  // IMPORTANT: Update these question titles to match your actual form questions
  for (var i = 0; i < itemResponses.length; i++) {
    var itemResponse = itemResponses[i];
    var question = itemResponse.getItem().getTitle();
    var answer = itemResponse.getResponse();
    
    // Map questions to fields (customize these based on your form)
    if (question.toLowerCase().includes("name")) {
      leadData.customer_name = answer;
    } else if (question.toLowerCase().includes("email")) {
      leadData.email = answer;
    } else if (question.toLowerCase().includes("phone") || question.toLowerCase().includes("mobile")) {
      leadData.phone = answer;
    } else if (question.toLowerCase().includes("service")) {
      leadData.service = answer;
    } else if (question.toLowerCase().includes("message") || question.toLowerCase().includes("details")) {
      leadData.message = answer;
    }
  }
  
  // Send to CRM
  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(leadData),
    "muteHttpExceptions": true
  };
  
  try {
    var response = UrlFetchApp.fetch(webhookUrl, options);
    Logger.log("Lead sent to CRM: " + response.getContentText());
  } catch (error) {
    Logger.log("Error sending to CRM: " + error);
  }
}
```

### Step 3: Configure the Webhook URL

In the script above, replace `http://localhost:8000` with your actual CRM backend URL:
- **Local development**: `http://localhost:8000`
- **Production**: Your deployed backend URL (e.g., `https://your-domain.com`)

### Step 4: Set Up the Trigger

1. In the Script Editor, click the **clock icon** (Triggers) in the left sidebar
2. Click **+ Add Trigger** in the bottom right
3. Configure the trigger:
   - Choose which function to run: `onFormSubmit`
   - Choose which deployment should run: `Head`
   - Select event source: `From form`
   - Select event type: `On form submit`
4. Click **Save**
5. Authorize the script when prompted

### Step 5: Test the Integration

1. Submit a test response to your Google Form
2. Check your CRM's Leads page - the new lead should appear
3. Check the Script Editor's **Executions** tab to see if the script ran successfully

## Troubleshooting

### Script Not Running
- Check the **Executions** tab in Script Editor for errors
- Verify the trigger is properly configured
- Make sure you've authorized the script

### Leads Not Appearing in CRM
- Verify your webhook URL is correct
- Check that your CRM backend is running and accessible
- Review the Script Editor logs (View → Logs)
- Ensure your form question titles match the mapping in the script

### Field Mapping Issues
- Update the question matching logic in the script to match your exact form questions
- The script uses `.toLowerCase().includes()` for flexible matching
- You can also use exact question titles for more precise mapping

## Form Question Mapping

The script maps form questions to CRM fields based on keywords. Update these mappings based on your actual form:

| Form Question Contains | Maps to CRM Field |
|------------------------|-------------------|
| "name" | customer_name |
| "email" | email |
| "phone" or "mobile" | phone |
| "service" | service |
| "message" or "details" | message |

## Next Steps

Once the integration is working:
1. All form submissions will automatically create leads in your CRM
2. New leads will trigger welcome emails (if configured)
3. You can manage all leads from the CRM's Leads page
4. Status updates will trigger appropriate email notifications
