//This is where the agent "TruthAgent" lives.
// We use "tracing" here so one can
//see when an API call starts and when
//it ends

use serde::{Deserialize,Serialize};
use anyhow::{Context,Result};
use reqwest::Client;
use tracing::{info, instrument};

#[derive(Serialize)]
struct GeminiRequest {
    model: String,
    messages: Vec<Message>,
}

#[derive(Serialize)]
struct Message {
    role: String,
    content: String,
}


//From an architecture point of view (pov),
#[derive(Deserialize, Debug)]
struct Choice{
    message: ResponseMessage,
}

#[derive(Deserialize,Debug)]
struct ResponseMessage
{
    content:String,
}


//2. The Logic Layer
pub struct TruthAgent
{
    client: Client,
    api_key: String,
}

impl TruthAgent {
    pub fn new (api_key:String) -> Self
    {
        Self
        {
            client: Client::new(),
            api_key,
        }
    }



    #[instrument(skip(self, transcript), fields(transcript_len = %transcript.len()))]
    pub async fn analyze_claims(&self,transcript:&str)-> Result<string>
    {
        info!();

        let url= "";
        let request_body= GeminiRequest {
            model: "gemini-3-flash".to_string(),
            messages: vec![
                Message {
                    role: "system".into(),
                    content: "Extract medical claims from the transcript. \
                    Rate truthfullness.".into()
                },

            ]
        }
    }


    pub async fn summarize_video_claims(&self,transcript:&str) -> Result<String>
    {
        //define url, define prompt --> LLM --> Get
        //Answer from API then unpack or deserialize the messages with serde

        let url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions";
        let prompt = format!(
            "Analayze the following video transcript for longevity or medical claims\
            Extract claims, timestamps, and scientific evidence mentionned\
            Transcript: {}", transcript);

        let request_body = GeminiRequest
        {
            model: "gemini-3-flash".to_string(), //2026 high-efficiency model
            messages: vec! [
                Message{role:"system".into(),content:"Extract medical claims ".into()},
                Message{role:"user".into(),content:transcript.to_string()},
            ],
        };

    }

}


//implement function analyze_claims here
