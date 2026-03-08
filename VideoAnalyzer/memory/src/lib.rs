//The lib.rs will be used to define the function which will then be input into main.rs
//main.rs

/*
Gaussian Temporal Function
score=e−^{(x−origin)^2}/2σ2

 Exponential Decay:
 score = e-^{(lambda*x)}
 */

pub fn gaussian_decay(x:f64,origin:f64,scale:f64)-> f64 {
    //Compute numerator, then denominator then compute them together
    let numerator = (x-origin).powi(2);
    let denominator =2.0*scale.powi(2);
    return (-numerator/denominator).exp();
}

//Need some test values here:


pub fn exponential_decay(x:f64,lambda:f64)->f64{
    return (-lambda*x).exp();
}

//Need some test values here:

/*
Here we can define the Rocchio formula or algorithm
The Rocchio algorithm is mostly used to push the vectors:

Score = Similarity(Q,D) + alpha*Sum(positives)- Beta*Sum(Negatives)
 How to build this formula?

 This is in a typical RAG System.

 let alpha:f64 = ;
 let beta:f64=;

 positives is vec<f64>
 negatives is vec<f64>. len(positives) = positives
 We have to compute the centroids of positives and negatives?

 So its just average of an array.

Formula: (Average Centroid). This is common in Rocchio Classification for
relevance feedback.
 */


pub fn relevance_feedback(){
    

}

//Find the average of an array or centroid of
// a list of values
pub fn get_average(values:&[f64]) -> f64 {
    //if len(values)==0:
    if values.is_empty(){
        return 0.0;
    }
    values.iter().sum::<f64>()/values.len() as f64
}

pub fn calculate_centroid_score(query_sim:f64,positives:&[f64],negatives:&[f64],alpha:f64,beta:f64) -> f64
{
    let pos_mean= get_average(positives);
    let neg_mean= get_average(negatives);
    query_sim+(alpha*pos_mean)-(beta*neg_mean)
}

