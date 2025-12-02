target "arm64-suv" {
  dockerfile = "arm64.Dockerfile" 
  tags = [
    "ghcr.io/xaatim/suv/arm64:v1"
  ]
  platforms = [
    "linux/arm64"
  ]
  provenance= false
  output = [
    { 
      type = "registry" 
    }
  ]
  context = "."
}
target "amd64-suv" {
  dockerfile = "amd64.Dockerfile" 
  tags = [
    "ghcr.io/xaatim/suv/amd64:v1"
  ]
  platforms = [
    "linux/amd64"
  ]
  provenance= false
  output = [
    { 
      type = "registry" 
    }
  ]
  context = "."
}

target "foxy-arm64-suv" {
  dockerfile = "foxy.Dockerfile" 
  tags = [
    "ghcr.io/xaatim/foxy/arm:v2"
  ]
  platforms = [
    "linux/arm64"
  ]
  provenance= false
  output = [
    { 
      type = "docker" 
    }
  ]
  context = "."
}

group "all" {
  targets = ["foxy-arm64-suv"]
}