output "instance_public_ip" {
  description = "AWS EC2 instance public IP adresi"
  value       = aws_instance.app.public_ip
}

output "instance_id" {
  description = "AWS EC2 instance ID"
  value       = aws_instance.app.id
}

output "app_url" {
  description = "FastAPI ve Docker uygulaması için adres"
  value       = "http://${aws_instance.app.public_ip}:8000"
}

output "ssh_command" {
  description = "EC2 instance'a bağlanmak için SSH komutu"
  value       = "ssh -i <private-key-path> ec2-user@${aws_instance.app.public_ip}"
}
