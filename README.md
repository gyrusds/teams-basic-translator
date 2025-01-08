# Teams Basic Translator

First steps into Teams and Azure bots. 

## Intro

This is a simple bot that connects to Gemini API to translate the last user message.

## Test the bot locally

### Prerequisites

* Python 3.11^.
* Poetry.
* Gemini API Key.

### Configuration

The bot requires the following environment variables to be set:

* `MicrosoftAppId`: The Microsoft App ID for the bot (blank in local testing).
* `MicrosoftAppPassword`: The Microsoft App Password for the bot (blank in local testing).
* `GOOGLE_API_KEY`: The API key for Google services.
* `TENANT`: The tenant name (use "common" for multi-tenant configuration).
* `HOST`: The host address for the bot (use `localhost` for local environments and `0.0.0.0` for cloud environments).

These must be set in a `.env` file in the root directory of the project.

### Install and run

```sh
poetry install
poetry run python bot/app.py
```

### Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

* Install the Bot Framework Emulator version 4.3.0 or greater from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect locally to the bot using Bot Framework Emulator

* Launch Bot Framework Emulator
* Enter a Bot URL of `http://localhost:8181/api/messages`

**Remember:** Ensure you are using port 8181.

## Test the bot in Azure

### Azure Prerequisites

* An Azure resource group where to create infraestructure elements.
* Enough permissions in that resource group.
* Active Directory App ID or User-Assigned Managed Identity Client ID.
* Azure cli installed.

### Steps

1. Create Web App for bot API (BotAPP).
2. Create Azure bot.
3. Deploy bot.
4. Test the bot.

### Creation of Azure elements

To test the bot on an Azure environment you need to create some elements prior to deploy bot code. To simplify this procees there are two templates with required configuration to create azure services via CLI. There are three infraestructure elements of azure needed to test the bot:

* An App Service plan to host a web application.
* A webapp in that service plan for the bot API (BotApp).
* An Azure Bot to create integrations.

The app service plan and the webapp are created with same [template-BotApp](infra/template-BotApp-with-rg.json). The Azure bot can be created using [template-AzureBot](/infra/template-AzureBot-with-rg.json).
**Important:** BotApp must be deployed prior to AzureBot.

Follow next steps to create all infraestructure.

#### Command line

``` sh
    az login
    az deployment group create --resource-group <group-name> --template-file <template-file> --parameters @<parameters-file>
```

#### Parameters for template-BotApp-with-rg.json

* **appServiceName**: (required)        The Name of the Bot App Service.
* (Pick an existing App Service Plan or create a new App Service Plan.)
  * **existingAppServicePlanName**:     The name of the App Service Plan.
  * **existingAppServicePlanLocation**: The location of the App Service Plan.
  * **newAppServicePlanName**:          The name of the App Service Plan.
  * **newAppServicePlanLocation**:      The location of the App Service Plan.
  * **newAppServicePlanSku**:           The SKU of the App Service Plan. Defaults to Standard values.
* **appType**:    Type of Bot Authentication. set as MicrosoftAppType in the Web App's Application Settings. **Allowed values are: MultiTenant(default), SingleTenant, UserAssignedMSI.**
* **appId**: (required)                                       Active Directory App ID or User-Assigned Managed Identity Client ID, set as MicrosoftAppId in the Web App's Application Settings.
* **appSecret**: (required for MultiTenant and SingleTenant)  Active Directory App Password, set as MicrosoftAppPassword in the Web App's Application Settings.
* **tenantId**:   The Azure AD Tenant ID to use as part of the Bot's Authentication. Only used for SingleTenant and UserAssignedMSI app types. Defaults to Subscription Tenant ID.

## Parameters for template-AzureBot-with-rg.json

* **azureBotId**: (required)          The globally unique and immutable bot ID.
* **azureBotSku**:                    The pricing tier of the Bot Service Registration. Allowed values are: F0, S1(default).
* **azureBotRegion**:                 Specifies the location of the new AzureBot. Allowed values are: global(default), westeurope.
* **botEndpoint**:                    Use to handle client messages, Such as `https://<botappServiceName>.azurewebsites.net/api/messages`.
* **appType**:   Type of Bot Authentication. set as MicrosoftAppType in the Web App's Application Settings. Allowed values are: MultiTenant(default), SingleTenant, UserAssignedMSI.
* **appId**: (required)                                       Active Directory App ID or User-Assigned Managed Identity Client ID, set as MicrosoftAppId in the Web App's Application Settings.
* **tenantId**:  The Azure AD Tenant ID to use as part of the Bot's Authentication. Only used for SingleTenant and UserAssignedMSI app types. Defaults to Subscription Tenant ID.

### How to deploy bot

Once,To deploy the bot to an Azure Web App, follow these steps:

1. Change to the `bot/` directory:

    ```sh
    cd bot/
    ```

2. Create a zip file for deployment:

    ```sh
    zip -r deploy.zip .
    ```

3. Deploy the generated zip file to your Azure Web App:

    ```sh
    az webapp deploy --src-path deploy.zip --resource-group <your-resource-group> --name <your-webapp-name> --type zip
    ```

Replace `<your-resource-group>` with your Azure resource group name and `<your-webapp-name>` with your Azure Web App name.

Finally, **remember to create GOOGLE_API_KEY environment variable on azure WebApp Service to be able to communicate with Google Gemini.**

## Further reading

* [Bot Framework Documentation](https://docs.botframework.com)
* [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
* [Dialogs](https://docs.microsoft.com/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0)
* [Gathering Input Using Prompts](https://docs.microsoft.com/azure/bot-service/bot-builder-prompts?view=azure-bot-service-4.0&tabs=csharp)
* [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
* [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
* [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
* [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest)
* [Azure Portal](https://portal.azure.com)
* [Language Understanding using LUIS](https://docs.microsoft.com/azure/cognitive-services/luis/)
* [Channels and Bot Connector Service](https://docs.microsoft.com/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)