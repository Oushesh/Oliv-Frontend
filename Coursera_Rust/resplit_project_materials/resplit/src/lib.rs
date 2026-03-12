use std::io::{BufReader,BufRead};
use clap::Parser; 

pub struct Cli {
	#[arg(short('f'))]
	field:usize,
	#[arg(short('d'))]
	delimeter: String,
	#[arg(long)]
	debug:bool,
}

pub fn read_stdin() -> String {
	let stdin = std::io::stdin();
	let mut reader  = BufReader::new(stdin.lock());
	let mut line = String::new();
	reader.read_line(&mut line).expect("Failed to read input line");
	line.trim().to_string()
}

pub fn splt(s: String, cli:&Cli)
{
	let parts: Vec<&str> = s.split(&cli.delimeter).collect();
	if cli.debug 
	{
		println!("Parts: {:?}", parts);
		println!("Indexes available at 0: {}",parts.len());

	}
	parts.get(cli.field).unwrap_or(&"").to_string()
} 



//Trim in Rust remove trailing spaces. 

/*
Example Code: 

fn main () {
	// create some strings
	let string 1 = " Welcome to Edpresso    "; 
	let string 2 = "Educative is the best!     "; 
	let string 3 = "     Rust is very interesting!"; 

	//trim the strings
	let trim1 = string1.trim();
	let trim2 = string2.trim();
	let trim3 = string3.trim();


	/ print the trims
  println!("The string before trim is '{}' and length is {}", string1, string1.len());
  println!("The string when trimmed is '{}' and length is {}", trim1, trim1.len());

  println!("\nThe string before trim is '{}' and length is {}", string2, string2.len());
  println!("The string when trimmed is '{}' and length is {}", trim2, trim2.len());

  println!("\nThe string before trim is '{}' and length is {}", string3, string3.len());
  println!("The string when trimmed is '{}' and length is {}", trim3, trim3.len());

}


*/