use video_truth_agent::TruthAgent; //import from your lib.rs
use anyhow::Result;


#[tokio::main]
async fn main() -> Result<()>
{
    //1. Initialize Logging
    tracing_subscriber::fmt::init();

    //2. Load Config
    dotenvy::dotenv().ok();
    let api_key = std::env::var("GEMINI_API_KEY")?;

    //what's the difference between ? and the the expect of rust in coding

    //3. Initialize Agent
    let agent = TruthAgent::new(api_key);

    //4. Run (Simulated transcript for now)
    let transcript = "Taking 1g of Vitamin C will prevent 100% of colds.";

    let report = agent.analyze_claims(transcript).await?; //output of analysis from the AI Agent
    println!("\n--- TRUTH REPORT ---\n{}",report);
    Ok(())

}

//modified main function to accommodate pinging the API and
//and getting the results


