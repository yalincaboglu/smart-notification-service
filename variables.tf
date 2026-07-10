variable "aws_region" {
  description = "AWS bölgesi"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance türü"
  type        = string
  default     = "t3.micro"
}

variable "ssh_key_name" {
  description = "AWS EC2 key pair adı"
  type        = string
  default     = "smart-notification-key"
}

variable "ssh_public_key_path" {
  description = "SSH public key dosya yolu (mutlaka tam yol yazın)"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "repo_url" {
  description = "GitHub / Git repo URL'si (deploy için)"
  type        = string
  default     = "https://github.com/YOUR_USER/smart-notification.git"
}

variable "repo_branch" {
  description = "Klone edilecek repo dalı"
  type        = string
  default     = "main"
}

variable "instance_name" {
  description = "EC2 instance adı"
  type        = string
  default     = "smart-notification-instance"
}

variable "allowed_ip_cidr" {
  description = "Güvenlik grubu için izin verilen IP bloğu"
  type        = string
  default     = "0.0.0.0/0"
}
