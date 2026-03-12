//2 ways to hand tests. inside the main.rs as "unit Test"
// or separate folder --> useful when app and code grows

//This tells Rust to only Compile this block when you r
//a cargo test

use axum::{body::Body, http::{Request, StatusCode}};
use tower::ServiceExt;
// Import from your library crate
use memory::{create_app};
use serde_json::json;

#[tokio::test]
async fn test_health_check() {
    let app = create_app(); // This now has a concrete type the compiler can infer

    let response = app
        .oneshot(
            Request::builder()
                .uri("/health")
                .body(Body::empty())
                .unwrap()
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

//Similarly we can test
#[tokio::test]
async fn test_calculate_api_logic() 
{
    let app = create_app();
    let response = app.oneshot(
        Request::builder()
            .method("POST")
            .uri("/calculate")
            .header("Content-Type", "application/json")
            .body(Body::from(json!(
                {
                            "query_sim": 0.5,
                            "positives": [1.0],
                            "negatives": [0.0],
                            "alpha": 0.1,
                            "beta": 0.05
                }
            ).to_string()))
            .unwrap(),
    ).await.unwrap();
    //perform an assertion in the question
    assert_eq!(response.status(), StatusCode::OK);
}


