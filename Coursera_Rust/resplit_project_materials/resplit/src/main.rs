//Call the functions from the lib.rs here
use resplit::Cli;
use clap::Parser;

fn main() 
{


    let cli = Cli::parse();
    let buffer = resplit::read_stdin();


    result = resplit::split(buffer, &cli);
    println!("The result is:{}",result);

}
