use axum::{routing::post,Json, Router};
use memory::{calculate_centroid_score, exponential_decay, gaussian_decay};
use serde::{Deserialize, Serialize};

pub mod utils; //this tells rust to look for a file named utils.rs

#[derive(Deserialize)]
struct SimilarityRequest {
    query_sim:f64,
    positives:Vec<f64>,
    negatives:Vec<f64>,
    alpha: f64,
    beta: f64,
}

#[derive(Serialize)]
struct SimilarityResponse {
    score: f64,
}

#[derive(Deserialize)]
struct GaussianDecayRequest {
    x:f64,
    origin:f64,
    scale:f64
}
#[derive(Serialize)]
struct GaussianDecayResponse {
    score:f64,
}

#[derive(Deserialize)]
struct ExponentialDecayRequest {
    x:f64,
    lambda:f64
}
#[derive(Serialize)]
struct ExponentialDecayResponse {
    score:f64,
}

/*
fn main() {
    println!("Hello, world!");
    let x:f64 = 2.0 ;
    let origin:f64 = 2.1;
    let scale:f64 = 2.0;

    //In rust main is expected to return nothing
    let result = memory::gaussian_decay(x,origin,scale);
    println!("The decay value is: {}",result);

    let query_sim:f64 =0.85;
    let positives: Vec<f64> =vec![0.9,0.8,0.75];
    let negatives:Vec<f64> = vec![0.2,0.1];
    let alpha:f64 = 0.1;
    let beta:f64 = 0.05;

    let centroid:f64= memory::calculate_centroid_score(query_sim,&positives,&negatives,alpha,beta);
    //query_sim:f64,positives:&[f64],negatives:&[f64
    //Add the centroid calculation here, then add it a database to see
    //how frontend can be connected here to actually perform the ranking
    //evaluation
    println!("The centroid value is: {}",centroid);
}
*/

//Convert those services into an API to serve for our customers

async fn api_calculate_similarity(Json(payload):Json<SimilarityRequest>) -> Json<SimilarityResponse>{
    let result = calculate_centroid_score(
        payload.query_sim,
        &payload.positives,
        &payload.negatives,
        payload.alpha,
        payload.beta
    );

    //Build the Json Output here:
    Json(SimilarityResponse{score: result})
}

async fn api_gaussian_decay(Json(payload):Json<GaussianDecayRequest>)->Json<GaussianDecayResponse>{
    let result = gaussian_decay(
        payload.x,
        payload.origin,
        payload.scale,
    );

    Json(GaussianDecayResponse{score:result})
}
async fn api_exponential_decay(Json(payload):Json<ExponentialDecayRequest>)->Json<ExponentialDecayResponse> {
    let result = exponential_decay(
        payload.x,
        payload.lambda,
    );
    Json(ExponentialDecayResponse{score:result})
}

#[tokio::main]
async fn main()
{
    println!("Hello, world!");
    /*
    let query_sim:f64 =0.85;
    let positives: Vec<f64> =vec![0.9,0.8,0.75];
    let negatives:Vec<f64> = vec![0.2,0.1];
    let alpha:f64 = 0.1;
    let beta:f64 = 0.05;
    */
    let app = Router::new()
        .route("/calculate",post(api_calculate_similarity))
        .route("/gaussian_decay", post(api_gaussian_decay))
        .route("/exponential_decay", post(api_exponential_decay));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    println!("Server running on 0.0.0.0:3000");
    axum::serve(listener,app).await.unwrap();
}

//Expanded or spun off 3 API to check (Nice) server worked properly.
//Now how to add test for health check of the APIs and then --> design the RAG system
//Database and stuffs

//