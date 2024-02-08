using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using CsvHelper;
using Newtonsoft.Json;

namespace JiraTicketCreator
{
  class Program
  {
    static HttpClient client = new HttpClient();
    private static readonly string jiraProjectKey = Environment.GetEnvironmentVariable("JIRA_PROJECT_KEY");

    static async Task Main(string[] args)
    {
      string jiraServer = Environment.GetEnvironmentVariable("JIRA_SERVER");
      string jiraUsername = Environment.GetEnvironmentVariable("JIRA_USERNAME");
      string jiraApiToken = Environment.GetEnvironmentVariable("JIRA_API_TOKEN");
      string templatesPath = Environment.GetEnvironmentVariable("TEMPLATES_PATH");
      if (templatesPath == null)
      {
        Environment.SetEnvironmentVariable("TEMPLATES_PATH", "templates");
      }

      if (string.IsNullOrEmpty(jiraServer) || string.IsNullOrEmpty(jiraUsername) || string.IsNullOrEmpty(jiraApiToken) || string.IsNullOrEmpty(templatesPath))
      {
        Console.WriteLine("Please set environment variables for JIRA_SERVER, JIRA_USERNAME, JIRA_API_TOKEN, and TEMPLATES_PATH.");
        return;
      }

      // Configure HttpClient
      client.BaseAddress = new Uri(jiraServer);
      client.DefaultRequestHeaders.Add("Authorization", $"Basic {Convert.ToBase64String(Encoding.ASCII.GetBytes($"{jiraUsername}:{jiraApiToken}"))}");
      client.DefaultRequestHeaders.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));

      await CreateTicketsAsync(templatesPath, null);
    }

    static async Task CreateTicketsAsync(string directory, string epicKey)
    {
      foreach (var item in Directory.GetFileSystemEntries(directory))
      {
        if (Directory.Exists(item))
        {
          string epicName = Path.GetFileName(item);
          string epicDescription = GetEpicDescription(Path.Combine(item, "description.txt"));
          string newEpicKey = await CreateEpicAsync(epicName, epicDescription);
          if (newEpicKey != null)
          {
            await CreateTicketsAsync(item, newEpicKey); // Recursively process nested folders
          }
        }
        else if (File.Exists(item) && item.EndsWith(".csv"))
        {
          using (var reader = new StreamReader(item))
          using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
          {
            var records = csv.GetRecords<dynamic>();
            foreach (var record in records)
            {
              string summary = record.Summary;
              string description = record.Description;
              await CreateTicketAsync(summary, description, epicKey);
            }
          }
        }
      }
    }

    static string GetEpicDescription(string descriptionFilePath)
    {
      if (File.Exists(descriptionFilePath))
      {
        return File.ReadAllText(descriptionFilePath);
      }
      else
      {
        // Return a default description if the file is not found
        return "Content to follow...";
      }
    }

    static async Task<string> CreateEpicAsync(string epicName, string description)
    {
      var epic = new
      {
        fields = new
        {
          project = new { key = jiraProjectKey },
          summary = epicName,
          description = description,
          issuetype = new { name = "Epic" }  // Change this to the appropriate issue type
        }
      };

      string json = JsonConvert.SerializeObject(epic);
      var content = new StringContent(json, Encoding.UTF8, "application/json");

      HttpResponseMessage response = await client.PostAsync("/rest/api/2/issue/", content);
      if (response.IsSuccessStatusCode)
      {
        string responseContent = await response.Content.ReadAsStringAsync();
        dynamic responseData = JsonConvert.DeserializeObject(responseContent);
        string epicKey = responseData.key;
        Console.WriteLine($"Epic created successfully: {epicKey}");
        return epicKey;
      }
      else
      {
        Console.WriteLine($"Failed to create epic: {response.StatusCode}");
        return null;
      }
    }

    static async Task CreateTicketAsync(string summary, string description, string epicKey)
    {
      var issue = new
      {
        fields = new
        {
          project = new { key = jiraProjectKey },
          summary = summary,
          description = description,
          issuetype = new { name = "Story" },  // Change this to the appropriate issue type
          parent = new { key = epicKey }
        }
      };

      string json = JsonConvert.SerializeObject(issue);
      var content = new StringContent(json, Encoding.UTF8, "application/json");

      HttpResponseMessage response = await client.PostAsync("/rest/api/2/issue/", content);
      if (response.IsSuccessStatusCode)
      {
        string responseContent = await response.Content.ReadAsStringAsync();
        dynamic responseData = JsonConvert.DeserializeObject(responseContent);
        string issueKey = responseData.key;
        Console.WriteLine($"Ticket created successfully: {issueKey}");
      }
      else
      {
        Console.WriteLine($"Failed to create ticket: {response.StatusCode}");
      }
    }
  }
}
